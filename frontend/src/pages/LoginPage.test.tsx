import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { LoginPage } from './LoginPage'
import { getAccessToken } from '../services/auth'


describe('LoginPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('logs in and navigates to characters', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        access_token: 'test-token',
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
        <MemoryRouter initialEntries={['/login']}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
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
      'player@example.com',
    )
    await user.type(
      screen.getByLabelText(/Password/i),
      'development-password',
    )
    await user.click(
      screen.getByRole('button', { name: 'Sign in' }),
    )

    expect(
      await screen.findByText('Characters page'),
    ).toBeInTheDocument()
    expect(getAccessToken()).toBe('test-token')
    expect(fetchMock).toHaveBeenCalledOnce()
  })
})