import { useState } from 'react'
import {
  Alert,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from '@mui/material'

import type {
  Resource,
  ResourceAction,
} from '../services/resources'


type ResourceCardProps = {
  resource: Resource
  isPending: boolean
  errorMessage?: string
  onChange: (
    resource: Resource,
    action: ResourceAction,
    amount: number,
  ) => void
}


export function ResourceCard({
  resource,
  isPending,
  errorMessage,
  onChange,
}: ResourceCardProps) {
  const [amount, setAmount] = useState(1)

  return (
    <Card>
      <CardContent>
        <Stack spacing={2}>
          <div>
            <Typography variant="h6">
              {resource.name}
            </Typography>

            <Typography color="text.secondary">
              {resource.source}
            </Typography>
          </div>

          <Typography variant="h4">
            {resource.current}
            {' / '}
            {resource.maximum}
          </Typography>

          <Typography
            variant="caption"
            color="text.secondary"
          >
            Recovers on:{' '}
            {resource.recovery_type
              .toLowerCase()
              .replaceAll('_', ' ')}
          </Typography>

          {errorMessage && (
            <Alert severity="error">
              {errorMessage}
            </Alert>
          )}

          <TextField
            label={`${resource.name} amount`}
            type="number"
            value={amount}
            onChange={(event) =>
              setAmount(Number(event.target.value))
            }
            slotProps={{
              htmlInput: {
                min: 0,
              },
            }}
            fullWidth
          />

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
              color="warning"
              variant="contained"
              disabled={isPending}
              onClick={() =>
                onChange(
                  resource,
                  'consume',
                  amount,
                )
              }
            >
              Consume {resource.name}
            </Button>

            <Button
              variant="outlined"
              disabled={isPending}
              onClick={() =>
                onChange(
                  resource,
                  'restore',
                  amount,
                )
              }
            >
              Restore {resource.name}
            </Button>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  )
}