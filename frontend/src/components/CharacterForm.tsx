import { type FormEvent, useState } from 'react'
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

import type {
  AbilityScores,
  CharacterCreate,
} from '../services/characters'


const PALADIN_SKILLS = [
  'athletics',
  'insight',
  'intimidation',
  'medicine',
  'persuasion',
  'religion',
]

const defaultCharacter: CharacterCreate = {
  name: '',
  level: 1,
  character_class: 'Paladin',
  species: '',
  background: '',
  abilities: {
    strength: 15,
    dexterity: 10,
    constitution: 14,
    intelligence: 8,
    wisdom: 12,
    charisma: 16,
  },
  hit_points: {
    maximum: 12,
    current: 12,
    temporary: 0,
  },
  saving_throw_proficiencies: [
    'wisdom',
    'charisma',
  ],
  skill_proficiencies: [],
  spellcasting_ability: 'charisma',
}

type CharacterFormProps = {
  title: string
  description: string
  submitLabel: string
  initialCharacter?: CharacterCreate
  isPending: boolean
  errorMessage?: string
  onSubmit: (character: CharacterCreate) => void
  onCancel: () => void
}

export function CharacterForm({
  title,
  description,
  submitLabel,
  initialCharacter = defaultCharacter,
  isPending,
  errorMessage,
  onSubmit,
  onCancel,
}: CharacterFormProps) {
  const [name, setName] = useState(initialCharacter.name)
  const [species, setSpecies] = useState(
    initialCharacter.species,
  )
  const [background, setBackground] = useState(
    initialCharacter.background,
  )
  const [level, setLevel] = useState(
    initialCharacter.level,
  )
  const [abilities, setAbilities] = useState({
    ...initialCharacter.abilities,
  })
  const [maximumHitPoints, setMaximumHitPoints] =
  useState(initialCharacter.hit_points.maximum)
  const [
    skillProficiencies,
    setSkillProficiencies,
  ] = useState([
    ...initialCharacter.skill_proficiencies,
  ])

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

    onSubmit({
      ...initialCharacter,
      name,
      level,
      species,
      background,
      abilities,
      hit_points: {
        maximum: maximumHitPoints,
        current: maximumHitPoints,
        temporary: 0,
      },
      skill_proficiencies: skillProficiencies,
    })
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
              {title}
            </Typography>
            <Typography color="text.secondary">
              {description}
            </Typography>
          </Box>

          {errorMessage && (
            <Alert severity="error">
              {errorMessage}
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
            <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
                label="Species"
                value={species}
                onChange={(event) =>
                setSpecies(event.target.value)
                }
                required
                fullWidth
            />
            </Grid>

            <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
                label="Background"
                value={background}
                onChange={(event) =>
                setBackground(event.target.value)
                }
                required
                fullWidth
            />
            </Grid>
          </Grid>
          <Box>
            <Typography variant="h5" sx={{ mb: 2 }}>
              Hit Points
            </Typography>
            <TextField
              label="Maximum hit points"
              type="number"
              value={maximumHitPoints}
              onChange={(event) =>
                setMaximumHitPoints(
                  Number(event.target.value),
                )
              }
              slotProps={{
                htmlInput: {
                  min: 1,
                },
              }}
              required
              fullWidth
            />
          </Box>
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
            <Button type="button" onClick={onCancel}>
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={isPending}
            >
              {submitLabel}
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Container>
  )
}