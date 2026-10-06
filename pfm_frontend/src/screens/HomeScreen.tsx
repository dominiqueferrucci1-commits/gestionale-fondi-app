import { useCallback, useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import { api } from '../api';
import type { Category, MonthlySummary, Strategy, Transaction } from '../types';

type Props = {
  onLogout: () => void;
};

const euro = (value: number) => `€ ${value.toFixed(2)}`;

export default function HomeScreen({ onLogout }: Props) {
  const [summary, setSummary] = useState<MonthlySummary | null>(null);
  const [strategy, setStrategy] = useState<Strategy | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    try {
      const [s, t, c, st] = await Promise.all([
        api.get<MonthlySummary>('/analytics/monthly'),
        api.get<Transaction[]>('/transactions'),
        api.get<Category[]>('/categories'),
        api.get<Strategy>('/strategies/recommendation'),
      ]);
      setSummary(s.data);
      setTransactions(t.data);
      setCategories(c.data);
      setStrategy(st.data);
      setError(null);
    } catch {
      setError('Impossibile contattare il server: avvia il backend e riprova.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const addTransaction = async () => {
    const value = parseFloat(amount.replace(',', '.'));
    if (!Number.isFinite(value) || value <= 0) {
      setError('Inserisci un importo valido maggiore di zero.');
      return;
    }
    if (categoryId === null) {
      setError('Seleziona una categoria.');
      return;
    }
    setSaving(true);
    try {
      await api.post('/transactions', {
        amount: value,
        category_id: categoryId,
        description: description.trim() || null,
      });
      setAmount('');
      setDescription('');
      setError(null);
      await load();
    } catch {
      setError('Salvataggio fallito: controlla i dati inseriti.');
    } finally {
      setSaving(false);
    }
  };

  const removeTransaction = (id: number) => {
    Alert.alert('Elimina transazione', 'Vuoi eliminare questa operazione?', [
      { text: 'Annulla', style: 'cancel' },
      {
        text: 'Elimina',
        style: 'destructive',
        onPress: async () => {
          await api.delete(`/transactions/${id}`);
          await load();
        },
      },
    ]);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#2563eb" />
        <Text style={styles.loadingText}>Caricamento dati…</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.brand}>Falko</Text>
        <TouchableOpacity onPress={onLogout}>
          <Text style={styles.logout}>Esci</Text>
        </TouchableOpacity>
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      {summary ? (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>
            Riepilogo {summary.month}/{summary.year}
          </Text>
          <View style={styles.summaryRow}>
            <View style={styles.summaryBox}>
              <Text style={styles.summaryLabel}>Entrate</Text>
              <Text style={[styles.summaryValue, styles.income]}>
                {euro(summary.total_income)}
              </Text>
            </View>
            <View style={styles.summaryBox}>
              <Text style={styles.summaryLabel}>Uscite</Text>
              <Text style={[styles.summaryValue, styles.expense]}>
                {euro(summary.total_expenses)}
              </Text>
            </View>
          </View>
          <View style={styles.summaryRow}>
            <View style={styles.summaryBox}>
              <Text style={styles.summaryLabel}>Avanzo</Text>
              <Text style={styles.summaryValue}>{euro(summary.net_balance)}</Text>
            </View>
            <View style={styles.summaryBox}>
              <Text style={styles.summaryLabel}>Risparmio</Text>
              <Text style={styles.summaryValue}>{summary.savings_rate}%</Text>
            </View>
          </View>
        </View>
      ) : null}

      {strategy ? (
        <View style={[styles.card, styles.strategyCard]}>
          <Text style={styles.cardTitle}>
            Strategia consigliata · {strategy.status}
          </Text>
          {strategy.recommendations.map((item) => (
            <View key={item.action_name} style={styles.recommendation}>
              <Text style={styles.recommendationName}>
                {item.action_name}
                {item.amount > 0 ? ` (${euro(item.amount)})` : ''}
              </Text>
              <Text style={styles.recommendationText}>{item.description}</Text>
            </View>
          ))}
        </View>
      ) : null}

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Nuova transazione</Text>

        <Text style={styles.label}>Importo</Text>
        <TextInput
          style={styles.input}
          keyboardType="decimal-pad"
          value={amount}
          onChangeText={setAmount}
          placeholder="0.00"
          placeholderTextColor="#94a3b8"
        />

        <Text style={styles.label}>Descrizione</Text>
        <TextInput
          style={styles.input}
          value={description}
          onChangeText={setDescription}
          placeholder="Es. spesa al supermercato"
          placeholderTextColor="#94a3b8"
        />

        <Text style={styles.label}>Categoria</Text>
        <View style={styles.chips}>
          {categories.map((category) => {
            const selected = category.id === categoryId;
            return (
              <TouchableOpacity
                key={category.id}
                style={[styles.chip, selected && styles.chipSelected]}
                onPress={() => setCategoryId(category.id)}
              >
                <Text style={[styles.chipText, selected && styles.chipTextSelected]}>
                  {category.name}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        <TouchableOpacity
          style={[styles.button, saving && styles.buttonDisabled]}
          onPress={addTransaction}
          disabled={saving}
        >
          <Text style={styles.buttonText}>
            {saving ? 'Salvataggio…' : 'Aggiungi transazione'}
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Ultime operazioni</Text>
        {transactions.length === 0 ? (
          <Text style={styles.empty}>Nessuna transazione registrata.</Text>
        ) : (
          transactions
            .slice()
            .reverse()
            .map((transaction) => {
              const category = categories.find(
                (c) => c.id === transaction.category_id,
              );
              const isExpense = category?.type === 'expense';
              return (
                <TouchableOpacity
                  key={transaction.id}
                  style={styles.transaction}
                  onLongPress={() => removeTransaction(transaction.id)}
                >
                  <View style={styles.transactionInfo}>
                    <Text style={styles.transactionDesc}>
                      {transaction.description || category?.name || 'Operazione'}
                    </Text>
                    <Text style={styles.transactionMeta}>
                      {transaction.date} · {category?.name ?? '—'}
                    </Text>
                  </View>
                  <Text
                    style={[
                      styles.transactionAmount,
                      isExpense ? styles.expense : styles.income,
                    ]}
                  >
                    {isExpense ? '-' : '+'}
                    {euro(transaction.amount)}
                  </Text>
                </TouchableOpacity>
              );
            })
        )}
        <Text style={styles.hint}>Tieni premuto su una transazione per eliminarla</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f1f5f9',
  },
  content: {
    padding: 16,
    paddingBottom: 40,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f1f5f9',
  },
  loadingText: {
    marginTop: 12,
    color: '#475569',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  brand: {
    fontSize: 26,
    fontWeight: '800',
    color: '#2563eb',
  },
  logout: {
    color: '#dc2626',
    fontWeight: '600',
  },
  error: {
    color: '#dc2626',
    backgroundColor: '#fee2e2',
    borderRadius: 10,
    padding: 10,
    marginBottom: 12,
    fontSize: 13,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0f172a',
    marginBottom: 12,
  },
  summaryRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 10,
  },
  summaryBox: {
    flex: 1,
    backgroundColor: '#f8fafc',
    borderRadius: 12,
    padding: 12,
  },
  summaryLabel: {
    fontSize: 12,
    color: '#64748b',
    marginBottom: 4,
  },
  summaryValue: {
    fontSize: 17,
    fontWeight: '700',
    color: '#0f172a',
  },
  income: {
    color: '#16a34a',
  },
  expense: {
    color: '#dc2626',
  },
  strategyCard: {
    backgroundColor: '#eff6ff',
  },
  recommendation: {
    marginBottom: 10,
  },
  recommendationName: {
    fontWeight: '700',
    color: '#1e3a8a',
    fontSize: 14,
  },
  recommendationText: {
    color: '#334155',
    fontSize: 13,
    lineHeight: 18,
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
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 16,
  },
  chip: {
    borderRadius: 999,
    borderWidth: 1,
    borderColor: '#cbd5e1',
    paddingHorizontal: 14,
    paddingVertical: 8,
    backgroundColor: '#f8fafc',
  },
  chipSelected: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  chipText: {
    color: '#334155',
    fontSize: 13,
  },
  chipTextSelected: {
    color: '#ffffff',
    fontWeight: '700',
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
    fontSize: 15,
    fontWeight: '700',
  },
  transaction: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#e2e8f0',
  },
  transactionInfo: {
    flex: 1,
    paddingRight: 10,
  },
  transactionDesc: {
    fontSize: 14,
    fontWeight: '600',
    color: '#0f172a',
  },
  transactionMeta: {
    fontSize: 12,
    color: '#64748b',
    marginTop: 2,
  },
  transactionAmount: {
    fontSize: 15,
    fontWeight: '700',
  },
  empty: {
    color: '#64748b',
    fontSize: 14,
  },
  hint: {
    marginTop: 10,
    fontSize: 11,
    color: '#94a3b8',
    textAlign: 'center',
  },
});
