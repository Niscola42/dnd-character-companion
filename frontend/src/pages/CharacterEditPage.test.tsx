import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { CharacterEditPage } from './CharacterEditPage'
import { saveAccessToken } from '../services/auth'


const character = {
  id: 1,
  name: 'Arthur',
  level: 5,
  character_class: 'Paladin',
  portrait_url: null,
  abilities: {
    strength: 16,
    dexterity: 12,
    constitution: 14,
    intelligence: 8,
    wisdom: 10,
    charisma: 18,
  },
  hit_points: {
    maximum: 42,
    current: 31,
    temporary: 5,
  },
  saving_throw_proficiencies: [
    'wisdom',
    'charisma',
  ],
  skill_proficiencies: [
    'athletics',
    'persuasion',
  ],
  spellcasting_ability: 'charisma',
  ability_modifiers: {},
  saving_throw_modifiers: {},
  skill_modifiers: {},
  proficiency_bonus: 3,
  initiative: 1,
  passive_perception: 10,
  spell_attack_modifier: 7,
  spell_save_dc: 15,
}


describe('CharacterEditPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('loads and updates a character', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => character,
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          ...character,
          name: 'Arthur Pendragon',
        }),
      })

    vi.stubGlobal('fetch', fetchMock)
    saveAccessToken('test-token')

    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
        mutations: {
          retry: false,
        },
      },
    })
    const user = userEvent.setup()

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/characters/1/edit']}>
          <Routes>
            <Route
              path="/characters/:characterId/edit"
              element={<CharacterEditPage />}
            />
            <Route
              path="/characters/:characterId"
              element={<div>Character dashboard</div>}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    const nameInput = await screen.findByLabelText(
      /Character name/i,
    )
    await user.clear(nameInput)
    await user.type(nameInput, 'Arthur Pendragon')
    await user.click(
      screen.getByRole('button', {
        name: 'Save changes',
      }),
    )

    expect(
      await screen.findByText('Character dashboard'),
    ).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)

    const updateRequest = fetchMock.mock.calls[1][1]
    const body = JSON.parse(updateRequest.body)

    expect(updateRequest.method).toBe('PUT')
    expect(body.name).toBe('Arthur Pendragon')
  })
})