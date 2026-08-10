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
    proficiency_bonus: number
    initiative: number
    passive_perception: number
    spell_attack_modifier: number | null
    spell_save_dc: number | null
  }
  
  export async function fetchCharacters(): Promise<Character[]> {
    const token = getAccessToken()
  
    if (!token) {
      throw new Error('Authentication required')
    }
  
    const response = await fetch(`${API_URL}/characters`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  
    if (response.status === 401) {
      clearAccessToken()
      throw new Error('Your session has expired')
    }
  
    if (!response.ok) {
      throw new Error('Unable to load characters')
    }
  
    return response.json()
  }