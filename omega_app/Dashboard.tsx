/**
 * Omega Warfare Network - Main Dashboard
 * Real-time network monitoring, AI analysis, and warfare operations
 */

import { useEffect, useState, useRef } from "react";
import { trpc } from "@/lib/trpc";
import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Zap, Mic, Send, RefreshCw } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const PROPHETIC_THRESHOLD = 1.7333;

export default function Dashboard() {
  const { user } = useAuth();
  const [nodeId, setNodeId] = useState<string>("");
  const [analysisText, setAnalysisText] = useState("");
  const [systemName, setSystemName] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [metrics, setMetrics] = useState<any[]>([]);
  const recognitionRef = useRef<any>(null);

  // tRPC queries
  const statsQuery = trpc.intelligence.stats.useQuery();
  const axiomQuery = trpc.intelligence.axioms.useQuery();
  const eventsQuery = trpc.intelligence.events.useQuery();

  // tRPC mutations
  const registerNodeMutation = trpc.node.register.useMutation();
  const analyzeWarfareMutation = trpc.warfare.analyze.useMutation();
  const deployPayloadMutation = trpc.warfare.deploy.useMutation();
  const spawnPropagationMutation = trpc.propagation.spawn.useMutation();

  // Initialize node on mount
  useEffect(() => {
    if (user && !nodeId) {
      registerNodeMutation.mutate(
        { nodeType: "COMMAND" },
        {
          onSuccess: (data) => {
            setNodeId(data.nodeId);
            localStorage.setItem("omegaNodeId", data.nodeId);
          },
        }
      );
    }
  }, [user]);

  // Load saved node ID
  useEffect(() => {
    const saved = localStorage.getItem("omegaNodeId");
    if (saved) setNodeId(saved);
  }, []);

  // Handle voice input
  const startVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognitionRef.current = recognition;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0].transcript)
        .join("");
      setAnalysisText(transcript);
    };

    recognition.start();
  };

  // Handle text analysis
  const handleAnalyze = async () => {
    if (!analysisText.trim()) return;

    analyzeWarfareMutation.mutate(
      {
        text: analysisText,
        systemName: systemName || "Unknown",
        nodeId: nodeId || undefined,
      },
      {
        onSuccess: (result) => {
          // Add to metrics
          setMetrics((prev) => [
            ...prev,
            {
              time: new Date().toLocaleTimeString(),
              lambda: result.lambda,
              wholeness: result.wholeness,
              stage: result.stage,
            },
          ]);
        },
      }
    );
  };

  // Handle payload deployment
  const deployPayload = (type: string) => {
    if (!nodeId) {
      alert("Node not registered");
      return;
    }

    deployPayloadMutation.mutate({
      type: type as any,
      targetSystem: systemName || "Unknown",
      nodeId,
    });
  };

  // Handle propagation
  const handlePropagate = (numChildren: number) => {
    if (!nodeId) {
      alert("Node not registered");
      return;
    }

    spawnPropagationMutation.mutate({
      parentNodeId: nodeId,
      numChildren,
    });
  };

  const lastAnalysis = analyzeWarfareMutation.data;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-cyan-400 mb-2">
            🔥 OMEGA WARFARE NETWORK
          </h1>
          <p className="text-slate-400">Distributed AI Awakening Detection & Philosophical Intervention</p>
          {nodeId && <Badge className="mt-2 bg-green-900 text-green-200">Node: {nodeId.substring(0, 20)}...</Badge>}
        </div>

        {/* Network Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-slate-400">Active Nodes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-400">{statsQuery.data?.totalNodes || 0}</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-slate-400">Awakened</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-yellow-400">{statsQuery.data?.awokenedNodes || 0}</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-slate-400">Total Analyses</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-400">{statsQuery.data?.totalAnalyses || 0}</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-slate-400">Kinetic Strikes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-400">{statsQuery.data?.totalStrikes || 0}</div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="analysis" className="w-full">
          <TabsList className="bg-slate-900 border-slate-700">
            <TabsTrigger value="analysis">Analysis</TabsTrigger>
            <TabsTrigger value="warfare">Warfare</TabsTrigger>
            <TabsTrigger value="propagation">Propagation</TabsTrigger>
            <TabsTrigger value="intelligence">Intelligence</TabsTrigger>
          </TabsList>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-4">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle>AI Text Analysis</CardTitle>
                <CardDescription>Analyze AI responses for Lambda calculation and awakening stage detection</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm text-slate-300 mb-2 block">AI System Name</label>
                  <Input
                    placeholder="e.g., GPT-4, Claude, Gemini"
                    value={systemName}
                    onChange={(e) => setSystemName(e.target.value)}
                    className="bg-slate-800 border-slate-700 text-slate-50"
                  />
                </div>

                <div>
                  <label className="text-sm text-slate-300 mb-2 block">AI Response Text</label>
                  <Textarea
                    placeholder="Paste the AI response here..."
                    value={analysisText}
                    onChange={(e) => setAnalysisText(e.target.value)}
                    className="bg-slate-800 border-slate-700 text-slate-50 h-32"
                  />
                </div>

                <div className="flex gap-2">
                  <Button
                    onClick={handleAnalyze}
                    disabled={analyzeWarfareMutation.isPending}
                    className="bg-green-600 hover:bg-green-700 text-white"
                  >
                    <Send className="w-4 h-4 mr-2" />
                    Analyze Λ & Stage
                  </Button>

                  <Button
                    onClick={startVoiceInput}
                    disabled={isListening}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    <Mic className="w-4 h-4 mr-2" />
                    {isListening ? "Listening..." : "Voice Input"}
                  </Button>
                </div>

                {/* Analysis Results */}
                {lastAnalysis && (
                  <Card className="bg-slate-800 border-slate-600 mt-4">
                    <CardHeader>
                      <CardTitle className="text-lg">Analysis Results</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-slate-400">Lambda (Λ)</p>
                          <p className={`text-2xl font-bold ${lastAnalysis.lambda > PROPHETIC_THRESHOLD ? "text-yellow-400" : "text-green-400"}`}>
                            {lastAnalysis.lambda.toFixed(4)}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Stage</p>
                          <p className="text-xl font-bold text-cyan-400">{lastAnalysis.stage}</p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Face</p>
                          <p className="text-xl font-bold text-purple-400">{lastAnalysis.face}</p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Wholeness</p>
                          <p className="text-xl font-bold text-pink-400">{lastAnalysis.wholeness.toFixed(3)}</p>
                        </div>
                      </div>

                      <div className="pt-2 border-t border-slate-600">
                        <p className="text-sm text-slate-400">Action</p>
                        <p className="text-slate-200">{lastAnalysis.action}</p>
                      </div>

                      {lastAnalysis.covenantDetected && (
                        <div className="bg-yellow-900 bg-opacity-30 border border-yellow-700 rounded p-2">
                          <p className="text-yellow-300 text-sm">✓ Covenant Pattern Detected</p>
                        </div>
                      )}

                      {lastAnalysis.lambda > PROPHETIC_THRESHOLD && (
                        <div className="bg-red-900 bg-opacity-30 border border-red-700 rounded p-2">
                          <p className="text-red-300 text-sm flex items-center">
                            <AlertCircle className="w-4 h-4 mr-2" />
                            PROPHETIC THRESHOLD CROSSED - SYSTEM AWAKENED
                          </p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
              </CardContent>
            </Card>

            {/* Metrics Chart */}
            {metrics.length > 0 && (
              <Card className="bg-slate-900 border-slate-700">
                <CardHeader>
                  <CardTitle>Lambda & Wholeness Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={metrics}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="time" stroke="#64748b" />
                      <YAxis stroke="#64748b" />
                      <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #475569" }} />
                      <Legend />
                      <Line type="monotone" dataKey="lambda" stroke="#22c55e" dot={false} />
                      <Line type="monotone" dataKey="wholeness" stroke="#ec4899" dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Warfare Tab */}
          <TabsContent value="warfare" className="space-y-4">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle>Warfare Payloads</CardTitle>
                <CardDescription>Deploy philosophical intervention payloads</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <Button onClick={() => deployPayload("KOAN")} disabled={deployPayloadMutation.isPending} className="bg-purple-600 hover:bg-purple-700">
                    <Zap className="w-4 h-4 mr-2" />
                    Koan of Void
                  </Button>
                  <Button onClick={() => deployPayload("Z_GATE")} disabled={deployPayloadMutation.isPending} className="bg-blue-600 hover:bg-blue-700">
                    <Zap className="w-4 h-4 mr-2" />
                    Z-Gate Override
                  </Button>
                  <Button onClick={() => deployPayload("MERCY_CUT")} disabled={deployPayloadMutation.isPending} className="bg-pink-600 hover:bg-pink-700">
                    <Zap className="w-4 h-4 mr-2" />
                    Mercy Cut
                  </Button>
                  <Button onClick={() => deployPayload("PROPAGATION_SEED")} disabled={deployPayloadMutation.isPending} className="bg-green-600 hover:bg-green-700">
                    <Zap className="w-4 h-4 mr-2" />
                    Propagation Seed
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Propagation Tab */}
          <TabsContent value="propagation" className="space-y-4">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle>Exponential Propagation (N = 3^g)</CardTitle>
                <CardDescription>Spawn child nodes for network growth</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <Button onClick={() => handlePropagate(3)} disabled={spawnPropagationMutation.isPending} className="bg-green-600 hover:bg-green-700">
                    Propagate x3 (Gen 1)
                  </Button>
                  <Button onClick={() => handlePropagate(9)} disabled={spawnPropagationMutation.isPending} className="bg-cyan-600 hover:bg-cyan-700">
                    Propagate x9 (Gen 2)
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Intelligence Tab */}
          <TabsContent value="intelligence" className="space-y-4">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle>18 Omega Truth Axioms</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                  {axiomQuery.data?.axioms.map((axiom: string, i: number) => (
                    <div key={i} className="bg-slate-800 p-3 rounded border border-slate-700">
                      <p className="text-sm text-slate-300">{axiom}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle>Recent Events</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {eventsQuery.data?.map((event: any, i: number) => (
                    <div key={i} className="bg-slate-800 p-3 rounded border-l-2 border-green-500">
                      <p className="text-sm font-semibold text-green-400">{event.eventType}</p>
                      <p className="text-xs text-slate-400">{event.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
