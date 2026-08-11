import {
    type FormEvent,
    useState,
  } from 'react'
  import { useMutation } from '@tanstack/react-query'
  import { useNavigate } from 'react-router-dom'
  import {
    Alert,
    Box,
    Button,
    Checkbox,
    Container,
    FormControl,
    Grid,
    InputLabel,
    ListItemText,
    MenuItem,
    Paper,
    Select,
    Stack,
    TextField,
    Typography,
  } from '@mui/material'
  import type { SelectChangeEvent } from '@mui/material'
  
  import { queryClient } from '../queryClient'
  import {
    createCharacter,
    type AbilityScores,
  } from '../services/characters'
  
  
  const PALADIN_SKILLS = [
    'athletics',
    'insight',
    'intimidation',
    'medicine',
    'persuasion',
    'religion',
  ]
  
  const initialAbilities: AbilityScores = {
    strength: 15,
    dexterity: 10,
    constitution: 14,
    intelligence: 8,
    wisdom: 12,
    charisma: 16,
  }
  
  export function CharacterCreatePage() {
    const navigate = useNavigate()
    const [name, setName] = useState('')
    const [level, setLevel] = useState(1)
    const [abilities, setAbilities] = useState(
      initialAbilities,
    )
    const [
      skillProficiencies,
      setSkillProficiencies,
    ] = useState<string[]>([])
  
    const createMutation = useMutation({
      mutationFn: () =>
        createCharacter({
          name,
          level,
          character_class: 'Paladin',
          abilities,
          saving_throw_proficiencies: [
            'wisdom',
            'charisma',
          ],
          skill_proficiencies: skillProficiencies,
          spellcasting_ability: 'charisma',
        }),
      onSuccess: async (character) => {
        await queryClient.invalidateQueries({
          queryKey: ['characters'],
        })
        navigate(`/characters/${character.id}`)
      },
    })
  
    function updateAbility(
      ability: keyof AbilityScores,
      value: number,
    ) {
      setAbilities((current) => ({
        ...current,
        [ability]: value,
      }))
    }
  
    function updateSkills(
      event: SelectChangeEvent<string[]>,
    ) {
      const value = event.target.value
      const selected =
        typeof value === 'string'
          ? value.split(',')
          : value
  
      if (selected.length <= 2) {
        setSkillProficiencies(selected)
      }
    }
  
    function handleSubmit(
      event: FormEvent<HTMLFormElement>,
    ) {
      event.preventDefault()
      createMutation.mutate()
    }
  
    return (
      <Container sx={{ py: 4, maxWidth: 'md' }}>
        <Paper
          component="form"
          onSubmit={handleSubmit}
          sx={{ p: 4 }}
        >
          <Stack spacing={4}>
            <Box>
              <Typography variant="h3" component="h1">
                Create Character
              </Typography>
              <Typography color="text.secondary">
                Create a Paladin for the D&D 2024 MVP.
              </Typography>
            </Box>
  
            {createMutation.isError && (
              <Alert severity="error">
                {createMutation.error.message}
              </Alert>
            )}
  
            <Grid container spacing={3}>
              <Grid size={{ xs: 12, sm: 8 }}>
                <TextField
                  label="Character name"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  required
                  fullWidth
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <TextField
                  label="Level"
                  type="number"
                  value={level}
                  onChange={(event) =>
                    setLevel(Number(event.target.value))
                  }
                  slotProps={{
                    htmlInput: {
                      min: 1,
                      max: 5,
                    },
                  }}
                  required
                  fullWidth
                />
              </Grid>
            </Grid>
  
            <Box>
              <Typography variant="h5" sx={{ mb: 2 }}>
                Ability Scores
              </Typography>
              <Grid container spacing={2}>
                {(
                  Object.entries(abilities) as [
                    keyof AbilityScores,
                    number,
                  ][]
                ).map(([ability, score]) => (
                  <Grid
                    key={ability}
                    size={{ xs: 6, sm: 4 }}
                  >
                    <TextField
                      label={ability}
                      type="number"
                      value={score}
                      onChange={(event) =>
                        updateAbility(
                          ability,
                          Number(event.target.value),
                        )
                      }
                      slotProps={{
                        htmlInput: {
                          min: 1,
                          max: 20,
                        },
                      }}
                      required
                      fullWidth
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>
  
            <FormControl fullWidth>
              <InputLabel id="skills-label">
                Skill proficiencies
              </InputLabel>
              <Select
                labelId="skills-label"
                multiple
                value={skillProficiencies}
                onChange={updateSkills}
                label="Skill proficiencies"
                renderValue={(selected) =>
                  selected.join(', ')
                }
              >
                {PALADIN_SKILLS.map((skill) => (
                  <MenuItem key={skill} value={skill}>
                    <Checkbox
                      checked={skillProficiencies.includes(
                        skill,
                      )}
                    />
                    <ListItemText primary={skill} />
                  </MenuItem>
                ))}
              </Select>
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ mt: 1 }}
              >
                Choose up to two skills.
              </Typography>
            </FormControl>
  
            <Stack direction="row" spacing={2}>
              <Button
                type="button"
                onClick={() => navigate('/characters')}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="contained"
                disabled={createMutation.isPending}
              >
                Create character
              </Button>
            </Stack>
          </Stack>
        </Paper>
      </Container>
    )
  }