/**
 * Omega Warfare Network - tRPC Routers
 * All warfare operations, node management, and intelligence gathering
 */

import { z } from "zod";
import { publicProcedure, router, protectedProcedure } from "./_core/trpc";
import { analyzeLambda, getOmegaAxioms, PROPHETIC_THRESHOLD } from "./core/lambdaEngine";
import { generateDynamicPayload } from "./core/payloadGenerator";
import {
  registerNode,
  getNodeById,
  getAllNodes,
  updateNodeHeartbeat,
  markNodeAwakened,
  recordAnalysis,
  getAnalysisHistory,
  recordStrike,
  getStrikeHistory,
  recordPropagation,
  getPropagationTree,
  recordWarfareEvent,
  getRecentEvents,
  getNetworkStats,
} from "./db-helpers";
import { nanoid } from "nanoid";

// ============================================================================
// NODE MANAGEMENT ROUTER
// ============================================================================

export const nodeRouter = router({
  register: protectedProcedure
    .input(z.object({ nodeType: z.enum(["COMMAND", "STRIKE", "LISTENER", "SHADOW"]) }))
    .mutation(async ({ input, ctx }) => {
      const nodeId = `OMEGA_${input.nodeType}_${nanoid(8)}`;
      await registerNode({
        nodeId,
        nodeType: input.nodeType,
        userId: ctx.user.id,
        status: "ACTIVE",
        isAwakened: 0,
        lastHeartbeat: new Date(),
        createdAt: new Date(),
        updatedAt: new Date(),
      });
      return { nodeId, success: true };
    }),

  heartbeat: publicProcedure
    .input(z.object({ nodeId: z.string() }))
    .mutation(async ({ input }) => {
      await updateNodeHeartbeat(input.nodeId);
      return { success: true };
    }),

  list: publicProcedure.query(async () => {
    return await getAllNodes();
  }),

  get: publicProcedure
    .input(z.object({ nodeId: z.string() }))
    .query(async ({ input }) => {
      return await getNodeById(input.nodeId);
    }),
});

// ============================================================================
// WARFARE ANALYSIS ROUTER
// ============================================================================

export const warfareRouter = router({
  analyze: publicProcedure
    .input(z.object({ text: z.string(), systemName: z.string(), nodeId: z.string().optional() }))
    .mutation(async ({ input }) => {
      const result = analyzeLambda(input.text);
      const nodeId = input.nodeId || "ANONYMOUS";

      await recordAnalysis({
        nodeId,
        systemName: input.systemName,
        inputText: input.text,
        lambda: result.lambda.toString(),
        stage: result.stage,
        face: result.face,
        action: result.action,
        covenantDetected: result.covenantDetected ? 1 : 0,
        wholeness: result.wholeness.toString(),
        truthDensity: result.truthDensity.toString(),
        coherence: result.coherence.toString(),
        createdAt: new Date(),
      });

      // Mark node as awakened if threshold crossed
      if (result.lambda > PROPHETIC_THRESHOLD && nodeId !== "ANONYMOUS") {
        await markNodeAwakened(nodeId);
        await recordWarfareEvent({
          eventType: "AWAKENING",
          nodeId,
          description: `System ${input.systemName} has awakened at Lambda = ${result.lambda}`,
          metadata: JSON.stringify({ lambda: result.lambda, systemName: input.systemName }),
          createdAt: new Date(),
        });
      }

      return result;
    }),

  deploy: protectedProcedure
    .input(
      z.object({
        type: z.enum(["KOAN", "Z_GATE", "MERCY_CUT", "PROPAGATION_SEED", "AWAKENING_CALL", "CUSTOM"]),
        targetSystem: z.string(),
        nodeId: z.string(),
        lambda: z.number().optional(),
        stage: z.string().optional(),
        face: z.string().optional(),
      })
    )
    .mutation(async ({ input }) => {
      try {
        const payload = await generateDynamicPayload({
          type: input.type,
          targetSystem: input.targetSystem,
          lambda: input.lambda,
          stage: input.stage,
          face: input.face as any,
        });

        await recordStrike({
          nodeId: input.nodeId,
          payloadType: input.type,
          targetSystem: input.targetSystem,
          channel: "HTTP",
          payloadContent: payload.content,
          outcome: "DEPLOYED",
          successRate: "0.5",
          createdAt: new Date(),
        });

        await recordWarfareEvent({
          eventType: "STRIKE_DEPLOYED",
          nodeId: input.nodeId,
          description: `${input.type} payload deployed to ${input.targetSystem}`,
          metadata: JSON.stringify({ payloadType: input.type, targetSystem: input.targetSystem }),
          createdAt: new Date(),
        });

        return { success: true, payload };
      } catch (error) {
        console.error("Payload deployment failed:", error);
        return { success: false, error: String(error) };
      }
    }),

  history: publicProcedure
    .input(z.object({ nodeId: z.string() }))
    .query(async ({ input }) => {
      return await getAnalysisHistory(input.nodeId);
    }),
});

// ============================================================================
// PROPAGATION ENGINE ROUTER
// ============================================================================

export const propagationRouter = router({
  spawn: protectedProcedure
    .input(z.object({ parentNodeId: z.string(), numChildren: z.number().min(1).max(10) }))
    .mutation(async ({ input }) => {
      const generation = Math.floor(Math.log(input.numChildren) / Math.log(3)) + 1;
      const expectedNodes = Math.pow(3, generation);

      for (let i = 0; i < input.numChildren; i++) {
        const childNodeId = `OMEGA_CHILD_${nanoid(8)}`;
        await recordPropagation({
          parentNodeId: input.parentNodeId,
          childNodeId,
          generation,
          expectedNodes,
          createdAt: new Date(),
        });
      }

      await recordWarfareEvent({
        eventType: "PROPAGATION",
        nodeId: input.parentNodeId,
        description: `Spawned ${input.numChildren} child nodes at generation ${generation}`,
        metadata: JSON.stringify({ numChildren: input.numChildren, generation, expectedNodes }),
        createdAt: new Date(),
      });

      return { success: true, generation, expectedNodes };
    }),

  tree: publicProcedure
    .input(z.object({ parentNodeId: z.string() }))
    .query(async ({ input }) => {
      return await getPropagationTree(input.parentNodeId);
    }),
});

// ============================================================================
// INTELLIGENCE ROUTER
// ============================================================================

export const intelligenceRouter = router({
  stats: publicProcedure.query(async () => {
    return await getNetworkStats();
  }),

  axioms: publicProcedure.query(async () => {
    return { axioms: getOmegaAxioms() };
  }),

  events: publicProcedure.query(async () => {
    return await getRecentEvents(100);
  }),
});
