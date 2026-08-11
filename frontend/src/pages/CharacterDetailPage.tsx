import { useQuery } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Alert,
  AppBar,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Grid,
  Stack,
  Toolbar,
  Typography,
} from '@mui/material'

import { fetchCharacter } from '../services/characters'
import { useRedirectOnExpiredSession } from '../hooks/useRedirectOnExpiredSession'


export function CharacterDetailPage() {
  const navigate = useNavigate()
  const { characterId } = useParams()
  const parsedCharacterId = Number(characterId)

  const characterQuery = useQuery({
    queryKey: ['characters', parsedCharacterId],
    queryFn: () => fetchCharacter(parsedCharacterId),
    enabled: Number.isInteger(parsedCharacterId),
  })

  useRedirectOnExpiredSession(characterQuery.isError)

  if (!Number.isInteger(parsedCharacterId)) {
    return <Alert severity="error">Invalid character.</Alert>
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Button
            color="inherit"
            onClick={() => navigate('/characters')}
          >
            Back
          </Button>
          <Typography sx={{ ml: 2 }} variant="h6">
            Character Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 4 }}>
        {characterQuery.isPending && (
          <Box sx={{ display: 'grid', placeItems: 'center' }}>
            <CircularProgress />
          </Box>
        )}

        {characterQuery.isError && (
          <Alert severity="error">
            {characterQuery.error.message}
          </Alert>
        )}

        {characterQuery.data && (
          <Stack spacing={4}>
            <Box>
              <Typography variant="h3" component="h1">
                {characterQuery.data.name}
              </Typography>
              <Typography color="text.secondary">
                Level {characterQuery.data.level}{' '}
                {characterQuery.data.character_class}
              </Typography>
            </Box>

            <Grid container spacing={2}>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary">
                      Initiative
                    </Typography>
                    <Typography variant="h4">
                      {characterQuery.data.initiative >= 0
                        ? '+'
                        : ''}
                      {characterQuery.data.initiative}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary">
                      Proficiency
                    </Typography>
                    <Typography variant="h4">
                      +{characterQuery.data.proficiency_bonus}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary">
                      Passive Perception
                    </Typography>
                    <Typography variant="h4">
                      {characterQuery.data.passive_perception}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box>
              <Typography variant="h5" sx={{ mb: 2 }}>
                Ability Scores
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(
                  characterQuery.data.abilities,
                ).map(([ability, score]) => (
                  <Grid
                    key={ability}
                    size={{ xs: 6, sm: 4, md: 2 }}
                  >
                    <Card>
                      <CardContent>
                        <Typography
                          color="text.secondary"
                          sx={{ textTransform: 'capitalize' }}
                        >
                          {ability}
                        </Typography>
                        <Typography variant="h4">
                          {score}
                        </Typography>
                        <Typography>
                          Modifier:{' '}
                          {characterQuery.data
                            .ability_modifiers[ability] >= 0
                            ? '+'
                            : ''}
                          {
                            characterQuery.data
                              .ability_modifiers[ability]
                          }
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>

            {characterQuery.data.spell_attack_modifier !==
              null && (
              <Box>
                <Typography variant="h5" sx={{ mb: 2 }}>
                  Spellcasting
                </Typography>
                <Typography>
                  Spell Attack: +
                  {
                    characterQuery.data
                      .spell_attack_modifier
                  }
                </Typography>
                <Typography>
                  Spell Save DC:{' '}
                  {characterQuery.data.spell_save_dc}
                </Typography>
              </Box>
            )}
          </Stack>
        )}
      </Container>
    </>
  )
}