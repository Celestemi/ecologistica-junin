export type GeoPoint = {
  type: "Point";
  coordinates: [number, number];
};

export type Order = {
  id: number;
  codigo_pedido: string;
  cliente_nombre: string;
  direccion_referencia: string;
  ubicacion: GeoPoint;
  altitud_msnm: number;
  peso_kg: number;
  ventana_inicio: string;
  ventana_fin: string;
  estado: string;
};

export type Vehicle = {
  id: number;
  deposito_id: number;
  placa: string;
  capacidad_kg: number;
  capacidad_m3: number;
  tipo_combustible: string;
  emision_base_co2_g_km: number;
  factor_penalizacion_pendiente: number;
  activo: boolean;
};

export type Depot = {
  id: number;
  nombre: string;
  direccion: string;
  ubicacion: GeoPoint;
  altitud_msnm: number;
};

export type FeatureProperties = {
  sequence?: number;
  stop_type?: string;
  plate?: string;
  order_code?: string | null;
  customer?: string | null;
  window_start?: string | null;
  window_end?: string | null;
  title?: string;
  co2_g?: number;
  eta?: string | null;
  kind?: string;
};

export type RouteFeature = {
  type: "Feature";
  geometry:
    | { type: "Point"; coordinates: [number, number] }
    | { type: "LineString"; coordinates: [number, number][] };
  properties: FeatureProperties;
};

export type RouteMetadata = {
  id: number;
  codigo: string;
  fecha_operacion: string;
  distancia_total_km: number;
  duracion_total_min: number;
  co2_estimado_kg: number;
  co2_referencia_kg: number;
  co2_evitado_kg: number;
  arboles_quinual_eq: number;
  quinual_kg_co2_por_ano: number;
  fitness: number;
  estado: string;
  feasible: boolean;
  pedidos: number;
  vehiculos_usados: number;
};

export type RouteOptimization = {
  type: "FeatureCollection";
  features: RouteFeature[];
  metadata: RouteMetadata;
};

export type DriverStop = {
  secuencia: number;
  tipo_parada: "depot_start" | "delivery" | "depot_end" | string;
  vehiculo_id: number;
  placa: string;
  codigo_pedido: string | null;
  cliente_nombre: string | null;
  direccion_referencia: string | null;
  peso_kg: number | null;
  ventana_inicio: string | null;
  ventana_fin: string | null;
  lat: number;
  lon: number;
  eta: string | null;
  co2_tramo_g: number;
};

export type ActiveRoute = {
  codigo: string;
  fecha_operacion: string;
  paradas: DriverStop[];
};

export type OrderTracking = {
  codigo_pedido: string;
  cliente_nombre: string;
  direccion_referencia: string;
  estado: string;
  lat: number;
  lon: number;
  ventana_inicio: string;
  ventana_fin: string;
  eta: string | null;
  paradas_previas: number;
  distancia_km: number;
  co2_tramo_g: number;
  co2_evitado_kg: number;
  placa: string | null;
  codigo_ruta: string | null;
};

export const HUANCAYO_CENTER: [number, number] = [-12.06513, -75.20486];

export const ROUTE_COLORS = ["#0f766e", "#9a3412", "#1d4ed8", "#a16207", "#6d28d9", "#be123c"];
