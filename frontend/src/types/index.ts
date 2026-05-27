export type AppRouteId = string;

export type EstadoModulo = "disponible" | "bloqueado" | "completado";

export interface Modulo {
  id: number;
  numero: number;
  titulo: string;
  descripcion: string;
  estado: EstadoModulo;
  progreso: number; // 0–100
  leccionesCompletadas?: number;
  leccionesTotales?: number;
}
