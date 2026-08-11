import {
  lazy,
  Suspense,
  type PropsWithChildren,
} from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'

import { getAccessToken } from './services/auth'


const LoginPage = lazy(() =>
  import('./pages/LoginPage').then((module) => ({
    default: module.LoginPage,
  })),
)

const CharacterListPage = lazy(() =>
  import('./pages/CharacterListPage').then((module) => ({
    default: module.CharacterListPage,
  })),
)

const CharacterCreatePage = lazy(() =>
  import('./pages/CharacterCreatePage').then((module) => ({
    default: module.CharacterCreatePage,
  })),
)

const CharacterDetailPage = lazy(() =>
  import('./pages/CharacterDetailPage').then((module) => ({
    default: module.CharacterDetailPage,
  })),
)

const RegisterPage = lazy(() =>
  import('./pages/RegisterPage').then((module) => ({
    default: module.RegisterPage,
  })),
)

const CharacterEditPage = lazy(() =>
  import('./pages/CharacterEditPage').then((module) => ({
    default: module.CharacterEditPage,
  })),
)

function ProtectedRoute({ children }: PropsWithChildren) {
  if (!getAccessToken()) {
    return <Navigate to="/login" replace />
  }

  return children
}


export default function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route
          path="/"
          element={<Navigate to="/login" replace />}
        />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/characters"
          element={
            <ProtectedRoute>
              <CharacterListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/characters/new"
          element={
            <ProtectedRoute>
              <CharacterCreatePage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/characters/:characterId/edit"
          element={
            <ProtectedRoute>
              <CharacterEditPage />
            </ProtectedRoute>
          }
        />

        <Route path="/register" element={<RegisterPage />} />

        <Route
          path="/characters/:characterId"
          element={
            <ProtectedRoute>
              <CharacterDetailPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="*"
          element={<Navigate to="/login" replace />}
        />
      </Routes>
    </Suspense>
  )
}