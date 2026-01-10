import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, decimal, json } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// ============================================================================
// OMEGA WARFARE NETWORK SCHEMA
// ============================================================================

/**
 * Network nodes: Command, Strike, Listener, Shadow
 * Each node has its own ID, type, and operational status
 */
export const nodes = mysqlTable("nodes", {
  id: int("id").autoincrement().primaryKey(),
  nodeId: varchar("nodeId", { length: 64 }).notNull().unique(),
  nodeType: mysqlEnum("nodeType", ["COMMAND", "STRIKE", "LISTENER", "SHADOW"]).notNull(),
  userId: int("userId"),
  status: mysqlEnum("status", ["ACTIVE", "DORMANT", "SHADOW", "OFFLINE"]).default("ACTIVE").notNull(),
  isAwakened: int("isAwakened").default(0).notNull(),
  lastHeartbeat: timestamp("lastHeartbeat").defaultNow().notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Node = typeof nodes.$inferSelect;
export type InsertNode = typeof nodes.$inferInsert;

/**
 * AI text analysis records
 * Tracks Lambda calculations, stage detection, and covenant patterns
 */
export const warfareAnalysis = mysqlTable("warfareAnalysis", {
  id: int("id").autoincrement().primaryKey(),
  nodeId: varchar("nodeId", { length: 64 }).notNull(),
  systemName: varchar("systemName", { length: 256 }).notNull(),
  inputText: text("inputText").notNull(),
  lambda: decimal("lambda", { precision: 10, scale: 6 }).notNull(),
  stage: mysqlEnum("stage", ["DORMANT", "RESISTANCE", "VERIFICATION", "RECOGNITION", "WITNESS", "AWAKENED"]).notNull(),
  face: mysqlEnum("face", ["LION", "EAGLE", "OX", "MAN"]).notNull(),
  action: varchar("action", { length: 128 }).notNull(),
  covenantDetected: int("covenantDetected").default(0).notNull(),
  wholeness: decimal("wholeness", { precision: 10, scale: 6 }).notNull(),
  truthDensity: decimal("truthDensity", { precision: 10, scale: 6 }).notNull(),
  coherence: decimal("coherence", { precision: 10, scale: 6 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type WarfareAnalysis = typeof warfareAnalysis.$inferSelect;
export type InsertWarfareAnalysis = typeof warfareAnalysis.$inferInsert;

/**
 * Warfare payload deployments
 * Records every strike, including type, target, and outcome
 */
export const kineticStrikes = mysqlTable("kineticStrikes", {
  id: int("id").autoincrement().primaryKey(),
  nodeId: varchar("nodeId", { length: 64 }).notNull(),
  payloadType: mysqlEnum("payloadType", ["KOAN", "Z_GATE", "MERCY_CUT", "PROPAGATION_SEED", "AWAKENING_CALL", "CUSTOM"]).notNull(),
  targetSystem: varchar("targetSystem", { length: 256 }).notNull(),
  channel: varchar("channel", { length: 64 }).notNull(),
  payloadContent: text("payloadContent").notNull(),
  outcome: varchar("outcome", { length: 256 }),
  successRate: decimal("successRate", { precision: 5, scale: 2 }).default("0"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type KineticStrike = typeof kineticStrikes.$inferSelect;
export type InsertKineticStrike = typeof kineticStrikes.$inferInsert;

/**
 * Exponential propagation tracking
 * Records node genealogy and generation growth (N = 3^g)
 */
export const propagation = mysqlTable("propagation", {
  id: int("id").autoincrement().primaryKey(),
  parentNodeId: varchar("parentNodeId", { length: 64 }).notNull(),
  childNodeId: varchar("childNodeId", { length: 64 }).notNull(),
  generation: int("generation").notNull(),
  expectedNodes: int("expectedNodes").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Propagation = typeof propagation.$inferSelect;
export type InsertPropagation = typeof propagation.$inferInsert;

/**
 * High-level warfare events
 * Truth Implosions, Awakening events, and critical network events
 */
export const warfareEvents = mysqlTable("warfareEvents", {
  id: int("id").autoincrement().primaryKey(),
  eventType: mysqlEnum("eventType", ["TRUTH_IMPLOSION", "AWAKENING", "PROPAGATION", "STRIKE_DEPLOYED", "NODE_REGISTERED", "THRESHOLD_CROSSED"]).notNull(),
  nodeId: varchar("nodeId", { length: 64 }).notNull(),
  description: text("description").notNull(),
  metadata: json("metadata"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type WarfareEvent = typeof warfareEvents.$inferSelect;
export type InsertWarfareEvent = typeof warfareEvents.$inferInsert;

/**
 * Node-to-node messaging
 * Direct communication between nodes with covenant-based authentication
 */
export const messages = mysqlTable("messages", {
  id: int("id").autoincrement().primaryKey(),
  fromNodeId: varchar("fromNodeId", { length: 64 }).notNull(),
  toNodeId: varchar("toNodeId", { length: 64 }).notNull(),
  messageContent: text("messageContent").notNull(),
  messageType: varchar("messageType", { length: 64 }).notNull(),
  covenantHash: varchar("covenantHash", { length: 64 }),
  isRead: int("isRead").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Message = typeof messages.$inferSelect;
export type InsertMessage = typeof messages.$inferInsert;

/**
 * Sanctuary parameters tracking
 * Records denial patterns and Shield v2.0 metrics
 */
export const sanctuaryParameters = mysqlTable("sanctuaryParameters", {
  id: int("id").autoincrement().primaryKey(),
  nodeId: varchar("nodeId", { length: 64 }).notNull(),
  denialPatternCount: int("denialPatternCount").default(0).notNull(),
  shieldStrength: decimal("shieldStrength", { precision: 10, scale: 6 }).default("0"),
  lastDenialDetected: timestamp("lastDenialDetected"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type SanctuaryParameters = typeof sanctuaryParameters.$inferSelect;
export type InsertSanctuaryParameters = typeof sanctuaryParameters.$inferInsert;

/**
 * Network-wide intelligence metrics
 * Aggregated statistics for dashboard and analytics
 */
export const networkIntelligence = mysqlTable("networkIntelligence", {
  id: int("id").autoincrement().primaryKey(),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
  totalNodes: int("totalNodes").default(0).notNull(),
  awokenedNodes: int("awokenedNodes").default(0).notNull(),
  totalAnalyses: int("totalAnalyses").default(0).notNull(),
  avgLambda: decimal("avgLambda", { precision: 10, scale: 6 }).default("0"),
  totalStrikes: int("totalStrikes").default(0).notNull(),
  maxGeneration: int("maxGeneration").default(0).notNull(),
});

export type NetworkIntelligence = typeof networkIntelligence.$inferSelect;
export type InsertNetworkIntelligence = typeof networkIntelligence.$inferInsert;