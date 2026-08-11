import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { CharacterCreatePage } from './CharacterCreatePage'
import { saveAccessToken } from '../services/auth'


describe('CharacterCreatePage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('creates a character and opens its dashboard', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({
        id: 7,
      }),
    })
    vi.stubGlobal('fetch', fetchMock)
    saveAccessToken('test-token')

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
        <MemoryRouter initialEntries={['/characters/new']}>
          <Routes>
            <Route
              path="/characters/new"
              element={<CharacterCreatePage />}
            />
            <Route
              path="/characters/:characterId"
              element={<div>Character dashboard</div>}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    await user.type(
      screen.getByLabelText(/Character name/i),
      'Galahad',
    )
    await user.click(
      screen.getByRole('button', {
        name: 'Create character',
      }),
    )

    expect(
      await screen.findByText('Character dashboard'),
    ).toBeInTheDocument()

    expect(fetchMock).toHaveBeenCalledOnce()

    const request = fetchMock.mock.calls[0][1]
    const body = JSON.parse(request.body)

    expect(body.name).toBe('Galahad')
    expect(body.character_class).toBe('Paladin')
    expect(body.saving_throw_proficiencies).toEqual([
      'wisdom',
      'charisma',
    ])
  })
})