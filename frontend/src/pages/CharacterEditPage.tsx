import { useMutation, useQuery } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Alert,
  Box,
  CircularProgress,
} from '@mui/material'

import { CharacterForm } from '../components/CharacterForm'
import { useRedirectOnExpiredSession } from '../hooks/useRedirectOnExpiredSession'
import { queryClient } from '../queryClient'
import {
  fetchCharacter,
  updateCharacter,
  type CharacterCreate,
} from '../services/characters'


export function CharacterEditPage() {
  const navigate = useNavigate()
  const { characterId } = useParams()
  const parsedCharacterId = Number(characterId)

  const characterQuery = useQuery({
    queryKey: ['characters', parsedCharacterId],
    queryFn: () => fetchCharacter(parsedCharacterId),
    enabled: Number.isInteger(parsedCharacterId),
  })

  const updateMutation = useMutation({
    mutationFn: (character: CharacterCreate) =>
      updateCharacter(
        parsedCharacterId,
        character,
      ),
    onSuccess: async (character) => {
      queryClient.setQueryData(
        ['characters', parsedCharacterId],
        character,
      )
      await queryClient.invalidateQueries({
        queryKey: ['characters'],
      })
      navigate(`/characters/${parsedCharacterId}`)
    },
  })

  useRedirectOnExpiredSession(
    characterQuery.isError
      || updateMutation.isError,
  )

  if (!Number.isInteger(parsedCharacterId)) {
    return <Alert severity="error">Invalid character.</Alert>
  }

  if (characterQuery.isPending) {
    return (
      <Box sx={{ display: 'grid', placeItems: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (characterQuery.isError) {
    return (
      <Alert severity="error">
        {characterQuery.error.message}
      </Alert>
    )
  }

  const character = characterQuery.data

  return (
    <CharacterForm
      title={`Edit ${character.name}`}
      description="Update the character's core information."
      submitLabel="Save changes"
      initialCharacter={{
        name: character.name,
        level: character.level,
        character_class: character.character_class,
        species: character.species ?? '',
        background: character.background ?? '',
        abilities: character.abilities,
        hit_points: character.hit_points,
        saving_throw_proficiencies:
          character.saving_throw_proficiencies,
        skill_proficiencies:
          character.skill_proficiencies,
        spellcasting_ability:
          character.spellcasting_ability,
      }}
      isPending={updateMutation.isPending}
      errorMessage={
        updateMutation.isError
          ? updateMutation.error.message
          : undefined
      }
      onSubmit={(updatedCharacter) =>
        updateMutation.mutate(updatedCharacter)
      }
      onCancel={() =>
        navigate(`/characters/${parsedCharacterId}`)
      }
    />
  )
}