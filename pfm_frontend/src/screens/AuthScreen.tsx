import { useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import { api, loginBody } from '../api';
import type { AuthTokens } from '../types';

type Props = {
  onAuthenticated: (tokens: AuthTokens) => void;
};

export default function AuthScreen({ onAuthenticated }: Props) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!email.trim() || !password) {
      setError('Inserisci email e password.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (mode === 'register') {
        await api.post('/auth/register', { email: email.trim(), password });
      }
      const { data } = await api.post<AuthTokens>(
        '/auth/login',
        loginBody(email.trim(), password),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } },
      );
      onAuthenticated(data);
    } catch (err) {
      const detail = (err as { response?: { data?: { detail?: string } } })
        .response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Connessione al server fallita.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.screen}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.card}>
        <Text style={styles.logo}>Falko</Text>
        <Text style={styles.title}>
          {mode === 'login' ? 'Accedi al tuo profilo' : 'Crea un nuovo profilo'}
        </Text>

        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          autoCapitalize="none"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
          placeholder="nome@esempio.com"
          placeholderTextColor="#94a3b8"
        />

        <Text style={styles.label}>Password</Text>
        <TextInput
          style={styles.input}
          secureTextEntry
          value={password}
          onChangeText={setPassword}
          placeholder="Minimo 8 caratteri"
          placeholderTextColor="#94a3b8"
        />

        {error ? <Text style={styles.error}>{error}</Text> : null}

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={submit}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#ffffff" />
          ) : (
            <Text style={styles.buttonText}>
              {mode === 'login' ? 'Accedi' : 'Registrati'}
            </Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => {
            setError(null);
            setMode(mode === 'login' ? 'register' : 'login');
          }}
        >
          <Text style={styles.switch}>
            {mode === 'login'
              ? 'Non hai un account? Registrati'
              : 'Hai già un account? Accedi'}
          </Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    padding: 24,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 24,
  },
  logo: {
    fontSize: 32,
    fontWeight: '800',
    color: '#2563eb',
    textAlign: 'center',
  },
  title: {
    fontSize: 16,
    color: '#475569',
    textAlign: 'center',
    marginTop: 4,
    marginBottom: 20,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: '#334155',
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: '#cbd5e1',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    color: '#0f172a',
    marginBottom: 14,
  },
  error: {
    color: '#dc2626',
    fontSize: 13,
    marginBottom: 10,
  },
  button: {
    backgroundColor: '#2563eb',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  switch: {
    color: '#2563eb',
    textAlign: 'center',
    marginTop: 16,
    fontSize: 14,
  },
});
