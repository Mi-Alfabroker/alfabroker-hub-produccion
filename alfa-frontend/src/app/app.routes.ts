import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/auth/pages/login-page/login-page').then(m => m.LoginPageComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/pages/dashboard-page/dashboard-page').then(m => m.DashboardPageComponent)
  },
  {
    path: 'aseguradoras',
    loadComponent: () => import('./features/aseguradoras/pages/aseguradoras-page/aseguradoras-page').then(m => m.AseguradorasPageComponent)
  },
  {
    path: 'mis-clientes',
    loadComponent: () => import('./features/mis-clientes/pages/mis-clientes-page/mis-clientes-page').then(m => m.MisClientesPageComponent)
  },
  {
    path: '**',
    redirectTo: ''
  }
];
