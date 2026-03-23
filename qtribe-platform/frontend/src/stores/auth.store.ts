import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, Tokens, AuthState } from '@app-types/index';
import { apiService } from '@services/api';

interface AuthStore extends AuthState {
  setUser: (user: User | null) => void;
  setTokens: (tokens: Tokens | null) => void;
  login: (user: User, tokens: Tokens) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,

      setUser: (user: User | null) => {
        set({ user, isAuthenticated: !!user });
      },

      setTokens: (tokens: Tokens | null) => {
        set({ tokens });
        if (tokens) {
          apiService.setAuthTokens(tokens);
        } else {
          apiService.clearAuth();
        }
      },

      login: (user: User, tokens: Tokens) => {
        set({ user, tokens, isAuthenticated: true });
        apiService.setAuthTokens(tokens);
      },

      logout: () => {
        set({ user: null, tokens: null, isAuthenticated: false });
        apiService.clearAuth();
      },

      updateUser: (userData: Partial<User>) => {
        const currentUser = get().user;
        if (currentUser) {
          set({ user: { ...currentUser, ...userData } });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
