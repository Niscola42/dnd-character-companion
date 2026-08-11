export const API_URL =
  import.meta.env.VITE_API_URL ??
  'http://127.0.0.1:8000/api'

const TOKEN_KEY = 'dnd-companion-access-token'

type LoginResponse = {
  access_token: string
  token_type: string
}

type RegisterResponse = {
    id: number
    email: string
  }

export async function login(
  email: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) {
    const body = await response.json()

    throw new Error(
      typeof body.detail === 'string'
        ? body.detail
        : 'Unable to sign in',
    )
  }

  return response.json()
}

export async function register(
    email: string,
    password: string,
  ): Promise<RegisterResponse> {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    })
  
    if (!response.ok) {
      const body = await response.json()
  
      throw new Error(
        typeof body.detail === 'string'
          ? body.detail
          : 'Unable to create account',
      )
    }
  
    return response.json()
  }

export function saveAccessToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function clearAccessToken() {
  localStorage.removeItem(TOKEN_KEY)
}