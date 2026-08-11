import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
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

import { clearAccessToken } from '../services/auth'
import { fetchCharacters } from '../services/characters'

export function CharacterListPage() {
  const navigate = useNavigate()
  const charactersQuery = useQuery({
    queryKey: ['characters'],
    queryFn: fetchCharacters,
  })

  function handleLogout() {
    clearAccessToken()
    navigate('/login')
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography sx={{ flexGrow: 1 }} variant="h6">
            D&D Character Companion
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Sign out
          </Button>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 4 }}>
        <Stack spacing={3}>
            <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={2}
                sx={{
                    justifyContent: 'space-between',
                    alignItems: {
                    xs: 'stretch',
                    sm: 'center',
                    },
                }}
                >
        <Box>
            <Typography variant="h3" component="h1">
            Your Characters
            </Typography>
            <Typography color="text.secondary">
            Choose a character to continue your adventure.
            </Typography>
        </Box>
        <Button
            variant="contained"
            onClick={() => navigate('/characters/new')}
        >
            Create character
        </Button>
        </Stack>

          {charactersQuery.isPending && (
            <Box sx={{ display: 'grid', placeItems: 'center' }}>
              <CircularProgress />
            </Box>
          )}

          {charactersQuery.isError && (
            <Alert severity="error">
              {charactersQuery.error.message}
            </Alert>
          )}

          {charactersQuery.data?.length === 0 && (
            <Alert severity="info">
              You do not have any characters yet.
            </Alert>
          )}

          <Grid container spacing={3}>
            {charactersQuery.data?.map((character) => (
              <Grid
                key={character.id}
                size={{ xs: 12, sm: 6, md: 4 }}
              >
                <Card>
                  <CardContent>
                    <Stack spacing={1}>
                      <Typography variant="h5">
                        {character.name}
                      </Typography>
                      <Typography color="text.secondary">
                        Level {character.level}{' '}
                        {character.character_class}
                      </Typography>
                      <Typography>
                        Initiative: {character.initiative >= 0
                          ? '+'
                          : ''}
                        {character.initiative}
                      </Typography>
                      <Typography>
                        Proficiency: +
                        {character.proficiency_bonus}
                      </Typography>
                      <Typography>
                        Passive Perception:{' '}
                        {character.passive_perception}
                      </Typography>

                      <Button
                        onClick={() =>
                            navigate(`/characters/${character.id}`)
                        }
                        >
                        Open dashboard
                        </Button>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Stack>
      </Container>
    </>
  )
}