import {
    useMutation,
    useQuery,
    useQueryClient,
  } from '@tanstack/react-query'
import { useState } from 'react'
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
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
} from '@mui/material'


import { CharacterPortrait } from '../components/CharacterPortrait'
import {
    performRest,
    type RestType,
  } from '../services/rests'
import { ResourceCard } from '../components/ResourceCard'
import {
    uploadCharacterPortrait,
    changeHitPoints,
    deleteCharacter,
    fetchCharacter,
    type HitPointAction,
  } from '../services/characters'
  import {
    changeResource,
    fetchResources,
    type Resource,
    type ResourceAction,
  } from '../services/resources'
import { useRedirectOnExpiredSession } from '../hooks/useRedirectOnExpiredSession'


export function CharacterDetailPage() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { characterId } = useParams()
  const parsedCharacterId = Number(characterId)
  const [deleteDialogOpen, setDeleteDialogOpen] =
  useState(false)
  const [hitPointAmount, setHitPointAmount] =
  useState(1)
  

  const characterQuery = useQuery({
    queryKey: ['characters', parsedCharacterId],
    queryFn: () => fetchCharacter(parsedCharacterId),
    enabled: Number.isInteger(parsedCharacterId),
  })

  const resourcesQuery = useQuery({
    queryKey: [
      'characters',
      parsedCharacterId,
      'resources',
    ],
    queryFn: () =>
      fetchResources(parsedCharacterId),
    enabled: Number.isInteger(parsedCharacterId),
  })

  const deleteMutation = useMutation({
    mutationFn: () =>
      deleteCharacter(parsedCharacterId),
    onSuccess: async () => {
        await queryClient.invalidateQueries({
          queryKey: ['characters'],
          exact: true,
        })
        navigate('/characters')
      },
  })
  
  const hitPointMutation = useMutation({
    mutationFn: ({
      action,
      amount,
    }: {
      action: HitPointAction
      amount: number
    }) =>
      changeHitPoints(
        parsedCharacterId,
        action,
        amount,
      ),
    onSuccess: (character) => {
      queryClient.setQueryData(
        ['characters', parsedCharacterId],
        character,
      )
    },
  })

  const resourceMutation = useMutation({
    mutationFn: ({
      resource,
      action,
      amount,
    }: {
      resource: Resource
      action: ResourceAction
      amount: number
    }) =>
      changeResource(
        parsedCharacterId,
        resource.id,
        action,
        amount,
      ),
    onSuccess: (updatedResource) => {
      queryClient.setQueryData<Resource[]>(
        [
          'characters',
          parsedCharacterId,
          'resources',
        ],
        (resources = []) =>
          resources.map((resource) =>
            resource.id === updatedResource.id
              ? updatedResource
              : resource,
          ),
      )
    },
  })

  const restMutation = useMutation({
    mutationFn: (restType: RestType) =>
      performRest(
        parsedCharacterId,
        restType,
      ),
      onSuccess: async () => {
        await queryClient.invalidateQueries({
          queryKey: [
            'characters',
            parsedCharacterId,
          ],
          exact: true,
        })
  
        await queryClient.invalidateQueries({
          queryKey: [
            'characters',
            parsedCharacterId,
            'resources',
          ],
          exact: true,
        })
      },
  })
  const portraitMutation = useMutation({
    mutationFn: (portrait: File) =>
      uploadCharacterPortrait(
        parsedCharacterId,
        portrait,
      ),
    onSuccess: (character) => {
      queryClient.setQueryData(
        ['characters', parsedCharacterId],
        character,
      )
    },
  })

  useRedirectOnExpiredSession(
    characterQuery.isError
      || resourcesQuery.isError
      || deleteMutation.isError
      || hitPointMutation.isError
      || portraitMutation.isError
      || restMutation.isError
      || resourceMutation.isError,
  )


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
            
            <Card
              sx={{
                overflow: 'hidden',
                borderColor: 'secondary.dark',
                background: `
                  linear-gradient(
                    120deg,
                    rgba(103, 21, 34, 0.42),
                    rgba(20, 17, 19, 0.96) 48%
                  )
                `,
              }}
            >
              <CardContent sx={{ p: { xs: 2, md: 4 } }}>
                <Grid container spacing={4}>
                  <Grid
                    size={{ xs: 12, md: 3 }}
                    sx={{
                      display: 'flex',
                      justifyContent: {
                        xs: 'center',
                        md: 'flex-start',
                      },
                    }}
                  >
                    <CharacterPortrait
                      name={characterQuery.data.name}
                      portraitUrl={
                        characterQuery.data.portrait_url
                      }
                      isPending={
                        portraitMutation.isPending
                      }
                      errorMessage={
                        portraitMutation.isError
                          ? portraitMutation.error.message
                          : undefined
                      }
                      onUpload={(portrait) =>
                        portraitMutation.mutate(portrait)
                      }
                    />
                  </Grid>

                  <Grid size={{ xs: 12, md: 9 }}>
                    <Stack spacing={3}>
                      <Box>
                        <Typography
                          variant="overline"
                          color="secondary.main"
                          sx={{
                            letterSpacing: '0.18em',
                          }}
                        >
                          Character Chronicle
                        </Typography>

                        <Typography
                          variant="h2"
                          component="h1"
                          sx={{
                            fontSize: {
                              xs: '2.8rem',
                              md: '4.5rem',
                            },
                            lineHeight: 1,
                            textTransform: 'uppercase',
                          }}
                        >
                          {characterQuery.data.name}
                        </Typography>

                        <Typography
                          color="text.secondary"
                          sx={{ mt: 1 }}
                        >
                          Level {characterQuery.data.level}{' '}
                          {characterQuery.data.character_class}
                        </Typography>
                      </Box>

                      <Stack
                        sx={{
                          flexDirection: {
                            xs: 'column',
                            sm: 'row',
                          },
                          gap: 1,
                        }}
                      >
                        <Button
                          variant="outlined"
                          onClick={() =>
                            navigate(
                              `/characters/${
                                parsedCharacterId
                              }/edit`,
                            )
                          }
                        >
                          Edit character
                        </Button>

                        <Button
                          color="error"
                          onClick={() =>
                            setDeleteDialogOpen(true)
                          }
                        >
                          Delete character
                        </Button>
                      </Stack>

                      <Grid container spacing={2}>
                        <Grid
                          size={{
                            xs: 12,
                            sm: 6,
                            lg: 3,
                          }}
                        >

                        </Grid>

                        <Grid
                          size={{
                            xs: 12,
                            sm: 6,
                            lg: 3,
                          }}
                        >
                          <Card sx={{ height: '100%' }}>
                            <CardContent>
                              <Typography
                                color="text.secondary"
                              >
                                Initiative
                              </Typography>
                              <Typography variant="h4">
                                {characterQuery.data
                                  .initiative >= 0
                                  ? '+'
                                  : ''}
                                {
                                  characterQuery.data
                                    .initiative
                                }
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>

                        <Grid
                          size={{
                            xs: 12,
                            sm: 6,
                            lg: 3,
                          }}
                        >
                          <Card sx={{ height: '100%' }}>
                            <CardContent>
                              <Typography
                                color="text.secondary"
                              >
                                Proficiency
                              </Typography>
                              <Typography variant="h4">
                                +
                                {
                                  characterQuery.data
                                    .proficiency_bonus
                                }
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>

                        <Grid
                          size={{
                            xs: 12,
                            sm: 6,
                            lg: 3,
                          }}
                        >
                          <Card sx={{ height: '100%' }}>
                            <CardContent>
                              <Typography
                                color="text.secondary"
                              >
                                Passive Perception
                              </Typography>
                              <Typography variant="h4">
                                {
                                  characterQuery.data
                                    .passive_perception
                                }
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                      </Grid>
                    </Stack>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            <Box>
              <Typography
                variant="overline"
                color="secondary.main"
                sx={{
                  letterSpacing: '0.18em',
                }}
              >
                Adventure Controls
              </Typography>

              <Typography variant="h4" sx={{ mb: 2 }}>
                Session Actions
              </Typography>

            
<Grid size={{ xs: 12, lg: 'auto' }}>
<Card
  sx={{
    width: {
      xs: '100%',
      lg: 'fit-content',
    },
    maxWidth: '100%',
  }}
>
    <CardContent>
      <Stack spacing={2}>

        {hitPointMutation.isError && (
          <Alert severity="error">
            {hitPointMutation.error.message}
          </Alert>
        )}

        <Grid
        container
        spacing={1.5}
        sx={{
            alignItems: 'center',
        }}
        >
<Grid size={{ xs: 12, sm: 'auto' }}>
  <Stack
    spacing={0.75}
    sx={{
      alignItems: {
        xs: 'stretch',
        sm: 'center',
      },
    }}
  >
    <Button
      size="small"
      color="success"
      variant="contained"
      disabled={hitPointMutation.isPending}
      onClick={() =>
        hitPointMutation.mutate({
          action: 'heal',
          amount: hitPointAmount,
        })
      }
      sx={{
        width: {
          xs: '100%',
          sm: 96,
        },
        minWidth: 0,
        minHeight: 28,
        px: 0.75,
        fontSize: '0.7rem',
      }}
    >
      Heal
    </Button>

    <TextField
      size="small"
      label="Amount"
      type="text"
      value={hitPointAmount}
      onChange={(event) => {
        const value = event.target.value

        if (/^\d*$/.test(value)) {
          setHitPointAmount(
            value === '' ? 0 : Number(value),
          )
        }
      }}
      slotProps={{
        htmlInput: {
          inputMode: 'numeric',
          pattern: '[0-9]*',
          'aria-label': 'Hit point amount',
          style: {
            padding: '6px 8px',
            textAlign: 'center',
            fontSize: '0.85rem',
          },
        },
        inputLabel: {
          shrink: true,
        },
      }}
      sx={{
        width: {
          xs: '100%',
          sm: 96,
        },
      }}
    />

    <Button
      size="small"
      color="error"
      variant="contained"
      disabled={hitPointMutation.isPending}
      onClick={() =>
        hitPointMutation.mutate({
          action: 'damage',
          amount: hitPointAmount,
        })
      }
      sx={{
        width: {
          xs: '100%',
          sm: 96,
        },
        minWidth: 0,
        minHeight: 28,
        px: 0.5,
        fontSize: '0.68rem',
      }}
    >
      Take damage
    </Button>
  </Stack>
</Grid>

          <Grid size={{ xs: 12, md: 'auto' }}>
          <Stack
  sx={{
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: {
      xs: 'center',
      md: 'flex-start',
    },
    flexWrap: {
      xs: 'wrap',
      sm: 'nowrap',
    },
    gap: 1.5,
  }}
>
  <Box>
    <Stack
      sx={{
        flexDirection: 'row',
        gap: 1,
      }}
    >
      <Box
      role="group"
      aria-label={
        `Current hit points: ${
          characterQuery.data.hit_points.current
        }`
      }
        sx={{
          width: 'fit-content',
          minWidth: 76,
          px: 1.5,
          py: 1,
          textAlign: 'center',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          bgcolor: (
            'rgba(255, 255, 255, 0.025)'
          ),
        }}
      >
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
          }}
        >
          Current
        </Typography>

        <Typography variant="h4">
          {
            characterQuery.data
              .hit_points.current
          }
        </Typography>
      </Box>

      <Box
      role="group"
      aria-label={
        `Maximum hit points: ${
          characterQuery.data.hit_points.maximum
        }`
      }
        sx={{
          width: 'fit-content',
          minWidth: 76,
          px: 1.5,
          py: 1,
          textAlign: 'center',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          bgcolor: (
            'rgba(255, 255, 255, 0.025)'
          ),
        }}
      >
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
          }}
        >
          Maximum
        </Typography>

        <Typography variant="h4">
          {
            characterQuery.data
              .hit_points.maximum
          }
        </Typography>
      </Box>
    </Stack>

    <Typography
      variant="h6"
      sx={{
        mt: 0.75,
        textAlign: 'center',
        color: 'secondary.main',
        textTransform: 'uppercase',
        letterSpacing: '0.12em',
        fontSize: '0.9rem',
      }}
    >
      Hit Points
    </Typography>
  </Box>

  <Box
  role="group"
  aria-label={
    `Temporary hit points: ${
      characterQuery.data.hit_points.temporary
    }`
  }
    sx={{
      width: 'fit-content',
      minWidth: 88,
      px: 1.5,
      py: 1,
      textAlign: 'center',
      border: '1px solid',
      borderColor: 'secondary.dark',
      borderRadius: 1,
      bgcolor: 'rgba(184, 150, 86, 0.05)',
    }}
  >
    <Typography
      variant="caption"
      color="text.secondary"
      sx={{
        textTransform: 'uppercase',
        letterSpacing: '0.06em',
      }}
    >
      Temporary
    </Typography>

    <Typography
      variant="h4"
      color="secondary.main"
    >
      {
        characterQuery.data
          .hit_points.temporary
      }
    </Typography>

    <Button
      size="small"
      variant="text"
      aria-label="Add temporary HP"
      disabled={hitPointMutation.isPending}
      onClick={() =>
        hitPointMutation.mutate({
          action: 'temporary',
          amount: hitPointAmount,
        })
      }
      sx={{
        minWidth: 0,
        mt: 0.25,
        px: 1,
        py: 0,
        fontSize: '0.7rem',
      }}
    >
      Add
    </Button>
  </Box>
</Stack> 
          </Grid>
        </Grid>
      </Stack>
    </CardContent>
  </Card>
</Grid>

              
            </Box>
            <Box>
            <Stack spacing={2} sx={{ mb: 2 }}>
  <Box>
    <Typography
      variant="overline"
      color="secondary.main"
      sx={{
        letterSpacing: '0.18em',
      }}
    >
      Powers & Supplies
    </Typography>

    <Stack
      sx={{
        flexDirection: {
          xs: 'column',
          sm: 'row',
        },
        alignItems: {
          xs: 'stretch',
          sm: 'center',
        },
        justifyContent: 'space-between',
        gap: 2,
      }}
    >
      <Box>
        <Typography variant="h4">
          Resources
        </Typography>

        <Typography color="text.secondary">
          Recover abilities and supplies during
          rests.
        </Typography>
      </Box>

      <Stack
        sx={{
          flexDirection: 'row',
          gap: 1,
          flexShrink: 0,
        }}
      >
        <Button
          size="small"
          variant="outlined"
          disabled={restMutation.isPending}
          onClick={() =>
            restMutation.mutate('SHORT')
          }
        >
          Short rest
        </Button>

        <Button
          size="small"
          variant="contained"
          disabled={restMutation.isPending}
          onClick={() =>
            restMutation.mutate('LONG')
          }
        >
          Long rest
        </Button>
      </Stack>
    </Stack>
  </Box>

  {restMutation.isError && (
    <Alert severity="error">
      {restMutation.error.message}
    </Alert>
  )}
</Stack>    
              {resourcesQuery.isPending && (
                <CircularProgress size={28} />
              )}

              {resourcesQuery.isError && (
                <Alert severity="error">
                  {resourcesQuery.error.message}
                </Alert>
              )}

              {resourcesQuery.data?.length === 0 && (
                <Alert severity="info">
                  This character has no resources yet.
                </Alert>
              )}

              <Grid container spacing={2}>
                {resourcesQuery.data?.map((resource) => (
                  <Grid
                    key={resource.id}
                    size={{ xs: 12, sm: 6 }}
                  >
                    <ResourceCard
                    resource={resource}
                    isPending={resourceMutation.isPending}
                    errorMessage={
                        resourceMutation.isError
                        && resourceMutation.variables.resource.id
                            === resource.id
                        ? resourceMutation.error.message
                        : undefined
                    }
                    onChange={(selected, action, amount) =>
                        resourceMutation.mutate({
                        resource: selected,
                        action,
                        amount,
                        })
                    }
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>

            <Dialog
              open={deleteDialogOpen}
              onClose={() => setDeleteDialogOpen(false)}
            >
              <DialogTitle>
                Delete character?
              </DialogTitle>

              <DialogContent>
                <DialogContentText>
                  This action permanently deletes the
                  character. It cannot be undone.
                </DialogContentText>

                {deleteMutation.isError && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {deleteMutation.error.message}
                  </Alert>
                )}
              </DialogContent>

              <DialogActions>
                <Button
                  onClick={() =>
                    setDeleteDialogOpen(false)
                  }
                  disabled={deleteMutation.isPending}
                >
                  Cancel
                </Button>

                <Button
                  color="error"
                  variant="contained"
                  onClick={() =>
                    deleteMutation.mutate()
                  }
                  disabled={deleteMutation.isPending}
                >
                  Delete permanently
                </Button>
              </DialogActions>
            </Dialog>   

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