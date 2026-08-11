import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { CharacterDetailPage } from './CharacterDetailPage'
import { saveAccessToken } from '../services/auth'


describe('CharacterDetailPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('shows derived statistics and returns to the list', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
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
        ability_modifiers: {
          strength: 3,
          dexterity: 1,
          constitution: 2,
          intelligence: -1,
          wisdom: 0,
          charisma: 4,
        },
        saving_throw_modifiers: {},
        skill_modifiers: {},
        proficiency_bonus: 3,
        initiative: 1,
        passive_perception: 10,
        spell_attack_modifier: 7,
        spell_save_dc: 15,
      }),
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
        <MemoryRouter initialEntries={['/characters/1']}>
          <Routes>
            <Route
              path="/characters/:characterId"
              element={<CharacterDetailPage />}
            />
            <Route
              path="/characters"
              element={<div>Character list</div>}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    expect(
      await screen.findByRole('heading', {
        name: 'Arthur',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Modifier: +3'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Spell Attack: +7'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Spell Save DC: 15'),
    ).toBeInTheDocument()

    await user.click(
      screen.getByRole('button', { name: 'Back' }),
    )

    expect(
      await screen.findByText('Character list'),
    ).toBeInTheDocument()
  })
})
