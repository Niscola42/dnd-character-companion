import {
    API_URL,
    clearAccessToken,
    getAccessToken,
  } from './auth'
  
  export type AbilityScores = {
    strength: number
    dexterity: number
    constitution: number
    intelligence: number
    wisdom: number
    charisma: number
  }
  
  export type Character = {
    id: number
    name: string
    level: number
    character_class: string
    abilities: AbilityScores
    ability_modifiers: Record<string, number>
    saving_throw_modifiers: Record<string, number>
    skill_modifiers: Record<string, number>
    proficiency_bonus: number
    initiative: number
    passive_perception: number
    spell_attack_modifier: number | null
    spell_save_dc: number | null
  }
  
  export type CharacterCreate = {
    name: string
    level: number
    character_class: string
    abilities: AbilityScores
    saving_throw_proficiencies: string[]
    skill_proficiencies: string[]
    spellcasting_ability: string | null
  }
  
  async function characterRequest<T>(
    path: string,
    options: RequestInit = {},
  ): Promise<T> {
    const token = getAccessToken()
  
    if (!token) {
      throw new Error('Authentication required')
    }
  
    const headers = new Headers(options.headers)
    headers.set('Authorization', `Bearer ${token}`)
  
    if (options.body) {
      headers.set('Content-Type', 'application/json')
    }
  
    const response = await fetch(
      `${API_URL}${path}`,
      {
        ...options,
        headers,
      },
    )
  
    if (response.status === 401) {
      clearAccessToken()
      throw new Error('Your session has expired')
    }
  
    if (!response.ok) {
      const body = await response.json()
  
      throw new Error(
        typeof body.detail === 'string'
          ? body.detail
          : 'Character request failed',
      )
    }
  
    return response.json()
  }
  
  export function fetchCharacters(): Promise<Character[]> {
    return characterRequest('/characters')
  }
  
  export function fetchCharacter(
    characterId: number,
  ): Promise<Character> {
    return characterRequest(`/characters/${characterId}`)
  }
  
  export function createCharacter(
    character: CharacterCreate,
  ): Promise<Character> {
    return characterRequest('/characters', {
      method: 'POST',
      body: JSON.stringify(character),
    })
  }