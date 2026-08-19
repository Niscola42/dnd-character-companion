import { afterEach, describe, expect, it, vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  MemoryRouter,
  Route,
  Routes,
} from 'react-router-dom'
import {
    render, 
    screen,
    waitFor,
 } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { CharacterDetailPage } from './CharacterDetailPage'
import { saveAccessToken } from '../services/auth'


describe('CharacterDetailPage', () => {
  afterEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  it('cancels and confirms character deletion', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          id: 2,
          name: 'Temporary Hero',
          level: 1,
          character_class: 'Paladin',
          portrait_url: null,
          abilities: {},
          hit_points: {
            maximum: 42,
            current: 31,
            temporary: 5,
          },
          ability_modifiers: {},
          saving_throw_modifiers: {},
          skill_modifiers: {},
          proficiency_bonus: 2,
          initiative: 0,
          passive_perception: 10,
          spell_attack_modifier: null,
          spell_save_dc: null,
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 204,
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
        <MemoryRouter initialEntries={['/characters/2']}>
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
  
    await screen.findByRole('heading', {
      name: 'Temporary Hero',
    })
  
    await user.click(
      screen.getByRole('button', {
        name: 'Delete character',
      }),
    )
    expect(
      screen.getByText('Delete character?'),
    ).toBeInTheDocument()
  
    await user.click(
      screen.getByRole('button', { name: 'Cancel' }),
    )
    await waitFor(() => {
      expect(
        screen.queryByText('Delete character?'),
      ).not.toBeInTheDocument()
    })
  
    await user.click(
      screen.getByRole('button', {
        name: 'Delete character',
      }),
    )
    await user.click(
      screen.getByRole('button', {
        name: 'Delete permanently',
      }),
    )
  
    expect(
      await screen.findByText('Character list'),
    ).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(3)
    expect(fetchMock.mock.calls[2][1].method).toBe('DELETE')
  })
  
  it('shows derived statistics and returns to the list', async () => {
    const fetchMock = vi
    .fn()
    .mockResolvedValueOnce({
        ok: true,
        status: 200,
      json: async () => ({
        id: 1,
        name: 'Arthur',
        level: 5,
        character_class: 'Paladin',
        species: 'Human',
        background: 'Soldier',
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

    .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [
          {
            id: 10,
            character_id: 1,
            name: 'Lay on Hands',
            source: 'Paladin',
            maximum: 25,
            current: 18,
            recovery_type: 'LONG_REST',
            metadata: {},
          },
          {
            id: 11,
            character_id: 1,
            name: 'Channel Divinity',
            source: 'Paladin',
            maximum: 2,
            current: 1,
            recovery_type: 'SHORT_REST',
            metadata: {},
          },
        ],
      })

    .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
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
            current: 26,
            temporary: 0,
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

    .mockResolvedValueOnce({
    ok: true,
    status: 200,
    json: async () => ({
        id: 10,
        character_id: 1,
        name: 'Lay on Hands',
        source: 'Paladin',
        maximum: 25,
        current: 15,
        recovery_type: 'LONG_REST',
        metadata: {},
    }),
    })

    .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          changes: [
            {
              name: 'Channel Divinity',
              before: 1,
              after: 2,
            },
          ],
          hit_points: null,
        }),
      })

      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
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
            current: 26,
            temporary: 0,
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
    .mockResolvedValueOnce({
    ok: true,
    status: 200,
    json: async () => [
        {
        id: 10,
        character_id: 1,
        name: 'Lay on Hands',
        source: 'Paladin',
        maximum: 25,
        current: 15,
        recovery_type: 'LONG_REST',
        metadata: {},
        },
        {
        id: 11,
        character_id: 1,
        name: 'Channel Divinity',
        source: 'Paladin',
        maximum: 2,
        current: 2,
        recovery_type: 'SHORT_REST',
        metadata: {},
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
        screen.getByText(
          'Human · Level 5 Paladin · Soldier',
        ),
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

    expect(
        await screen.findByRole('group', {
          name: 'Current hit points: 31',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Maximum hit points: 42',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Temporary hit points: 5',
        }),
      ).toBeInTheDocument()

    expect(
        await screen.findByText('Lay on Hands'),
      ).toBeInTheDocument()
  
      expect(
        screen.getByText('18 / 25'),
      ).toBeInTheDocument()
  
      expect(
        screen.getByText('Channel Divinity'),
      ).toBeInTheDocument()
  
      expect(
        screen.getByText('1 / 2'),
      ).toBeInTheDocument()

    const damageInput = screen.getByLabelText(
        'Hit point amount',
      )
  
      await user.clear(damageInput)
      await user.type(damageInput, '10')
      await user.click(
        screen.getByRole('button', {
          name: 'Take damage',
        }),
      )
  
      expect(
        await screen.findByRole('group', {
          name: 'Current hit points: 26',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Temporary hit points: 0',
        }),
      ).toBeInTheDocument()
  
      expect(fetchMock).toHaveBeenCalledTimes(3)
  
      const damageRequest = fetchMock.mock.calls[2][1]
      const damageBody = JSON.parse(damageRequest.body)
  
      expect(fetchMock.mock.calls[2][0]).toContain(
        '/characters/1/health/damage',
      )
      expect(damageRequest.method).toBe('POST')
      expect(damageBody).toEqual({ amount: 10 })

      const resourceInput = screen.getByLabelText(
        'Lay on Hands amount',
      )
  
      await user.clear(resourceInput)
      await user.type(resourceInput, '3')
      await user.click(
        screen.getByRole('button', {
          name: 'Consume Lay on Hands',
        }),
      )
  
      expect(
        await screen.findByText('15 / 25'),
      ).toBeInTheDocument()
  
      expect(fetchMock).toHaveBeenCalledTimes(4)
  
      const resourceRequest = fetchMock.mock.calls[3][1]
      const resourceBody = JSON.parse(
        resourceRequest.body,
      )
  
      expect(fetchMock.mock.calls[3][0]).toContain(
        '/characters/1/resources/10/consume',
      )
      expect(resourceRequest.method).toBe('POST')
      expect(resourceBody).toEqual({ amount: 3 })

      await user.click(
        screen.getByRole('button', {
          name: 'Short rest',
        }),
      )
  
      expect(
        await screen.findByText('2 / 2'),
      ).toBeInTheDocument()
  
      expect(fetchMock).toHaveBeenCalledTimes(7)
  
      const restRequest = fetchMock.mock.calls[4][1]
      const restBody = JSON.parse(restRequest.body)
  
      expect(fetchMock.mock.calls[4][0]).toContain(
        '/characters/1/rests',
      )
      expect(restRequest.method).toBe('POST')
      expect(restBody).toEqual({
        rest_type: 'SHORT',
      })    

    await user.click(
      screen.getByRole('button', { name: 'Back' }),
    )

    expect(
      await screen.findByText('Character list'),
    ).toBeInTheDocument()
  })

  it('performs a long rest and refreshes the dashboard', async () => {
    const initialCharacter = {
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
        current: 26,
        temporary: 5,
      },
      ability_modifiers: {
        strength: 3,
      },
      saving_throw_modifiers: {},
      skill_modifiers: {},
      saving_throw_proficiencies: [],
      skill_proficiencies: [],
      spellcasting_ability: 'charisma',
      proficiency_bonus: 3,
      initiative: 1,
      passive_perception: 10,
      spell_attack_modifier: 7,
      spell_save_dc: 15,
    }

    const restoredCharacter = {
      ...initialCharacter,
      hit_points: {
        maximum: 42,
        current: 42,
        temporary: 0,
      },
    }

    const initialResources = [
      {
        id: 10,
        character_id: 1,
        name: 'Lay on Hands',
        source: 'Paladin',
        maximum: 25,
        current: 15,
        recovery_type: 'LONG_REST',
        metadata: {},
      },
    ]

    const restoredResources = [
      {
        ...initialResources[0],
        current: 25,
      },
    ]

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => initialCharacter,
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => initialResources,
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          changes: [
            {
              name: 'Lay on Hands',
              before: 15,
              after: 25,
            },
          ],
          hit_points: {
            current_before: 26,
            current_after: 42,
            temporary_before: 5,
            temporary_after: 0,
          },
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => restoredCharacter,
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => restoredResources,
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
        <MemoryRouter initialEntries={['/characters/1']}>
          <Routes>
            <Route
              path="/characters/:characterId"
              element={<CharacterDetailPage />}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    expect(
        await screen.findByRole('group', {
          name: 'Current hit points: 26',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Maximum hit points: 42',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Temporary hit points: 5',
        }),
      ).toBeInTheDocument()

    expect(
      await screen.findByText('15 / 25'),
    ).toBeInTheDocument()

    await user.click(
      screen.getByRole('button', {
        name: 'Long rest',
      }),
    )

    expect(
        await screen.findByRole('group', {
          name: 'Current hit points: 42',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Maximum hit points: 42',
        }),
      ).toBeInTheDocument()
      
      expect(
        screen.getByRole('group', {
          name: 'Temporary hit points: 0',
        }),
      ).toBeInTheDocument()

    expect(
      await screen.findByText('25 / 25'),
    ).toBeInTheDocument()

    const restRequest = fetchMock.mock.calls[2][1]

    expect(fetchMock.mock.calls[2][0]).toContain(
      '/characters/1/rests',
    )
    expect(restRequest.method).toBe('POST')
    expect(JSON.parse(restRequest.body)).toEqual({
      rest_type: 'LONG',
    })
  })

  it('uploads and displays a character portrait', async () => {
    const characterWithoutPortrait = {
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
        current: 42,
        temporary: 0,
      },
      ability_modifiers: {
        strength: 3,
      },
      saving_throw_modifiers: {},
      skill_modifiers: {},
      saving_throw_proficiencies: [],
      skill_proficiencies: [],
      spellcasting_ability: 'charisma',
      proficiency_bonus: 3,
      initiative: 1,
      passive_perception: 10,
      spell_attack_modifier: 7,
      spell_save_dc: 15,
    }

    const uploadedCharacter = {
      ...characterWithoutPortrait,
      portrait_url: (
        '/uploads/characters/1/arthur.png'
      ),
    }

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => characterWithoutPortrait,
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => uploadedCharacter,
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

    const { container } = render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/characters/1']}>
          <Routes>
            <Route
              path="/characters/:characterId"
              element={<CharacterDetailPage />}
            />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    )

    expect(
      await screen.findByText('No portrait'),
    ).toBeInTheDocument()

    const fileInput = container.querySelector(
      'input[type="file"]',
    )

    expect(fileInput).not.toBeNull()

    const portrait = new File(
      ['image-content'],
      'arthur.png',
      {
        type: 'image/png',
      },
    )

    await user.upload(
      fileInput as HTMLInputElement,
      portrait,
    )

    const image = await screen.findByRole('img', {
      name: 'Arthur portrait',
    })

    expect(image).toHaveAttribute(
      'src',
      (
        'http://127.0.0.1:8000'
        + '/uploads/characters/1/arthur.png'
      ),
    )

    expect(fetchMock).toHaveBeenCalledTimes(3)

    const uploadRequest = fetchMock.mock.calls[2][1]

    expect(fetchMock.mock.calls[2][0]).toContain(
      '/characters/1/portrait',
    )
    expect(uploadRequest.method).toBe('POST')
    expect(uploadRequest.body).toBeInstanceOf(FormData)
    expect(uploadRequest.headers.get('Content-Type')).toBeNull()
  })

})
