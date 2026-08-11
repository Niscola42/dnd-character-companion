import { type FormEvent, useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import {
  Link as RouterLink,
  useNavigate,
} from 'react-router-dom'
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Link,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material'

import {
  login,
  register,
  saveAccessToken,
} from '../services/auth'


export function RegisterPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [
    passwordConfirmation,
    setPasswordConfirmation,
  ] = useState('')

  const registerMutation = useMutation({
    mutationFn: async () => {
      if (password !== passwordConfirmation) {
        throw new Error('Passwords do not match')
      }

      await register(email, password)

      return login(email, password)
    },
    onSuccess: (data) => {
      saveAccessToken(data.access_token)
      navigate('/characters')
    },
  })

  function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()
    registerMutation.mutate()
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'grid',
        placeItems: 'center',
        p: 2,
      }}
    >
      <Paper
        component="form"
        onSubmit={handleSubmit}
        sx={{ width: '100%', maxWidth: 420, p: 4 }}
      >
        <Stack spacing={3}>
          <Box>
            <Typography variant="h4" component="h1">
              Create Account
            </Typography>
            <Typography color="text.secondary">
              Start building your D&D characters.
            </Typography>
          </Box>

          {registerMutation.isError && (
            <Alert severity="error">
              {registerMutation.error.message}
            </Alert>
          )}

          <TextField
            label="Email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
            fullWidth
          />
          <TextField
            label="Password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            helperText="Use at least 8 characters."
            slotProps={{
              htmlInput: {
                minLength: 8,
              },
            }}
            required
            fullWidth
          />
          <TextField
            label="Confirm password"
            type="password"
            autoComplete="new-password"
            value={passwordConfirmation}
            onChange={(event) =>
              setPasswordConfirmation(
                event.target.value,
              )
            }
            required
            fullWidth
          />

          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={registerMutation.isPending}
          >
            {registerMutation.isPending ? (
              <CircularProgress size={24} />
            ) : (
              'Create account'
            )}
          </Button>

          <Typography sx={{ textAlign: 'center' }}>
            Already have an account?{' '}
            <Link component={RouterLink} to="/login">
              Sign in
            </Link>
          </Typography>
        </Stack>
      </Paper>
    </Box>
  )
}