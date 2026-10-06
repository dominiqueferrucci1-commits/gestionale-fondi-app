export type CategoryType = 'income' | 'expense';

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Category {
  id: number;
  name: string;
  type: CategoryType;
}

export interface Transaction {
  id: number;
  amount: number;
  date: string;
  description: string | null;
  category_id: number;
}

export interface MonthlySummary {
  year: number;
  month: number;
  total_income: number;
  total_expenses: number;
  net_balance: number;
  savings_rate: number;
}

export interface ActionPlanItem {
  action_name: string;
  amount: number;
  description: string;
}

export interface Strategy {
  net_balance: number;
  savings_rate: number;
  status: string;
  recommendations: ActionPlanItem[];
}
