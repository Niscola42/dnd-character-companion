import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import { getAccessToken } from '../services/auth'


export function useRedirectOnExpiredSession(
  requestFailed: boolean,
) {
  const navigate = useNavigate()

  useEffect(() => {
    if (requestFailed && !getAccessToken()) {
      navigate('/login', { replace: true })
    }
  }, [navigate, requestFailed])
}