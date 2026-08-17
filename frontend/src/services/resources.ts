import {
    API_URL,
    clearAccessToken,
    getAccessToken,
  } from './auth'
  
  
  export type RecoveryType =
    | 'SHORT_REST'
    | 'LONG_REST'
    | 'MANUAL'
  
  export type Resource = {
    id: number
    character_id: number
    name: string
    source: string
    maximum: number
    current: number
    recovery_type: RecoveryType
    metadata: Record<string, unknown>
  }
  
  
  async function resourceRequest<T>(
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
          : 'Resource request failed',
      )
    }
  
    return response.json()
  }
  
  
  export function fetchResources(
    characterId: number,
  ): Promise<Resource[]> {
    return resourceRequest(
      `/characters/${characterId}/resources`,
    )
  }

  export type ResourceAction =
  | 'consume'
  | 'restore'


export function changeResource(
  characterId: number,
  resourceId: number,
  action: ResourceAction,
  amount: number,
): Promise<Resource> {
  return resourceRequest(
    (
      `/characters/${characterId}`
      + `/resources/${resourceId}/${action}`
    ),
    {
      method: 'POST',
      body: JSON.stringify({ amount }),
    },
  )
}