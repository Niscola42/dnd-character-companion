import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { CharacterListPage } from './CharacterListPage'
import {
  getAccessToken,
  saveAccessToken,
} from '../services/auth'


describe('CharacterListPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('shows characters and signs out', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [
        {
          id: 1,
          name: 'Arthur',
          level: 5,
          character_class: 'Paladin',
          abilities: {
            strength: 16,
            dexterity: 12,
            constitution: 14,
            intelligence: 8,
            wisdom: 10,
            charisma: 18,
          },
          proficiency_bonus: 3,
          initiative: 1,
          passive_perception: 10,
          spell_attack_modifier: 7,
          spell_save_dc: 15,
        },
      ],
    })
    vi.stubGlobal('fetch', fetchMock)
    saveAccessToken('test-token')

    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    })
    const user = userEvent.setup()

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/characters']}>
          <Routes>
            <Route
              path="/characters"
              element={<CharacterListPage />}
            />
            <Route
              path="/login"
              element={<div>Login page</div>}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    expect(
      await screen.findByText('Arthur'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Initiative: +1'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Proficiency: +3'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Passive Perception: 10'),
    ).toBeInTheDocument()

    await user.click(
      screen.getByRole('button', { name: 'Sign out' }),
    )

    expect(
      await screen.findByText('Login page'),
    ).toBeInTheDocument()
    expect(getAccessToken()).toBeNull()
  })
})