import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'

import { CharacterForm } from '../components/CharacterForm'
import { useRedirectOnExpiredSession } from '../hooks/useRedirectOnExpiredSession'
import { queryClient } from '../queryClient'
import {
  createCharacter,
  type CharacterCreate,
} from '../services/characters'


export function CharacterCreatePage() {
  const navigate = useNavigate()

  const createMutation = useMutation({
    mutationFn: createCharacter,
    onSuccess: async (character) => {
      await queryClient.invalidateQueries({
        queryKey: ['characters'],
      })
      navigate(`/characters/${character.id}`)
    },
  })

  useRedirectOnExpiredSession(createMutation.isError)

  function handleSubmit(character: CharacterCreate) {
    createMutation.mutate(character)
  }

  return (
    <CharacterForm
      title="Create Character"
      description="Create a Paladin for the D&D 2024 MVP."
      submitLabel="Create character"
      isPending={createMutation.isPending}
      errorMessage={
        createMutation.isError
          ? createMutation.error.message
          : undefined
      }
      onSubmit={handleSubmit}
      onCancel={() => navigate('/characters')}
    />
  )
}