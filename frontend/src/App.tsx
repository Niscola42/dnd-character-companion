import { Navigate, Route, Routes } from 'react-router-dom'

import { CharacterListPage } from './pages/CharacterListPage'
import { LoginPage } from './pages/LoginPage'

import type { PropsWithChildren } from 'react'
import { getAccessToken } from './services/auth'


function ProtectedRoute({ children }: PropsWithChildren) {
  if (!getAccessToken()) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/characters"
        element={
          <ProtectedRoute>
            <CharacterListPage />
          </ProtectedRoute>
  }
/>
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}