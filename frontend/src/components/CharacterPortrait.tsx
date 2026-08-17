import type { ChangeEvent } from 'react'
import {
  Alert,
  Box,
  Button,
  Stack,
  Typography,
} from '@mui/material'

import { API_URL } from '../services/auth'


const API_ORIGIN = API_URL.replace(/\/api\/?$/, '')


type CharacterPortraitProps = {
  name: string
  portraitUrl: string | null
  isPending: boolean
  errorMessage?: string
  onUpload: (portrait: File) => void
}


export function CharacterPortrait({
  name,
  portraitUrl,
  isPending,
  errorMessage,
  onUpload,
}: CharacterPortraitProps) {
  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0]

    if (file) {
      onUpload(file)
    }

    event.target.value = ''
  }

  const imageUrl = portraitUrl
    ? `${API_ORIGIN}${portraitUrl}`
    : null

  return (
    <Stack spacing={2} sx={{ width: 220 }}>
      <Box
        sx={{
          aspectRatio: '3 / 4',
          overflow: 'hidden',
          borderRadius: 2,
          border: '1px solid',
          borderColor: 'secondary.dark',
          bgcolor: 'background.paper',
          display: 'grid',
          placeItems: 'center',
        }}
      >
        {imageUrl ? (
          <Box
            component="img"
            src={imageUrl}
            alt={`${name} portrait`}
            sx={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
          />
        ) : (
            <Typography
            color="text.secondary"
            sx={{
                px: 2,
                textAlign: 'center',
            }}
            >
            No portrait
          </Typography>
        )}
      </Box>

      {errorMessage && (
        <Alert severity="error">
          {errorMessage}
        </Alert>
      )}

      <Button
        component="label"
        variant="outlined"
        disabled={isPending}
      >
        {isPending
          ? 'Uploading...'
          : 'Choose portrait'}

        <input
          hidden
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileChange}
        />
      </Button>

      <Typography
        color="text.secondary"
        sx={{
            px: 2,
            textAlign: 'center',
        }}
        >
        JPEG, PNG or WebP · maximum 5 MB
      </Typography>
    </Stack>
  )
}