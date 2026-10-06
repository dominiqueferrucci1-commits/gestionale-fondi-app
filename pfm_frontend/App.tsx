import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';

import { clearAuthHeader, setAuthHeader } from './src/api';
import AuthScreen from './src/screens/AuthScreen';
import HomeScreen from './src/screens/HomeScreen';
import type { AuthTokens } from './src/types';

export default function App() {
  const [tokens, setTokens] = useState<AuthTokens | null>(null);

  if (!tokens) {
    return (
      <>
        <AuthScreen
          onAuthenticated={(next) => {
            setAuthHeader(next.access_token);
            setTokens(next);
          }}
        />
        <StatusBar style="light" />
      </>
    );
  }

  return (
    <>
      <HomeScreen
        onLogout={() => {
          clearAuthHeader();
          setTokens(null);
        }}
      />
      <StatusBar style="dark" />
    </>
  );
}
