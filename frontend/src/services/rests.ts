import {
    API_URL,
    clearAccessToken,
    getAccessToken,
  } from './auth'
  
  
  export type RestType = 'SHORT' | 'LONG'
  
  export type ResourceChange = {
    name: string
    before: number
    after: number
  }
  
  export type HitPointChange = {
    current_before: number
    current_after: number
    temporary_before: number
    temporary_after: number
  }
  
  export type RestSummary = {
    changes: ResourceChange[]
    hit_points: HitPointChange | null
  }
  
  
  export async function performRest(
    characterId: number,
    restType: RestType,
  ): Promise<RestSummary> {
    const token = getAccessToken()
  
    if (!token) {
      throw new Error('Authentication required')
    }
  
    const response = await fetch(
      `${API_URL}/characters/${characterId}/rests`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rest_type: restType,
        }),
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
          : 'Rest request failed',
      )
    }
  
    return response.json()
  }