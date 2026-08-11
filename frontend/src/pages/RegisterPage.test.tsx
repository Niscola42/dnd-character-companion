import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { RegisterPage } from './RegisterPage'
import { getAccessToken } from '../services/auth'


describe('RegisterPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('registers, logs in, and opens characters', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({
          id: 1,
          email: 'new-player@example.com',
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          access_token: 'new-token',
          token_type: 'bearer',
        }),
      })

    vi.stubGlobal('fetch', fetchMock)

    const queryClient = new QueryClient({
      defaultOptions: {
        mutations: {
          retry: false,
        },
      },
    })
    const user = userEvent.setup()

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/register']}>
          <Routes>
            <Route
              path="/register"
              element={<RegisterPage />}
            />
            <Route
              path="/characters"
              element={<div>Characters page</div>}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    await user.type(
      screen.getByLabelText(/Email/i),
      'new-player@example.com',
    )
    await user.type(
      screen.getByLabelText(/^Password/i),
      'a-secure-password',
    )
    await user.type(
      screen.getByLabelText(/Confirm password/i),
      'a-secure-password',
    )
    await user.click(
      screen.getByRole('button', {
        name: 'Create account',
      }),
    )

    expect(
      await screen.findByText('Characters page'),
    ).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
    expect(getAccessToken()).toBe('new-token')
  })
})
