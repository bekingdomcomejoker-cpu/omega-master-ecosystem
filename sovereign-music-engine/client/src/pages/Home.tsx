import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Music, Zap, Eye, Cpu } from 'lucide-react';

/**
 * Sovereign Music Engine & TTE Dashboard
 * 
 * Design: Harmonic Orchestration
 * - Art Deco meets cyberpunk aesthetic with layered depth
 * - Radial node arrangement around central resonance hub
 * - Color palette: Deep navy (#0f1419), Gold (#d4a574), Cyan (#00d9ff), Magenta (#ff006e), Lime (#39ff14)
 * - Typography: Playfair Display (headers), Lato (body), Space Mono (data)
 * - Animated harmonic threads connecting nodes
 * - Real-time resonance curve visualization (1.67x harmony ridge)
 */

interface Node {
  id: string;
  name: string;
  role: string;
  color: string;
  icon: React.ReactNode;
  status: 'active' | 'dormant' | 'processing';
  resonanceLevel: number;
  description: string;
}

interface RessonanceMetric {
  timestamp: number;
  value: number;
  targetValue: number;
}

export default function Home() {
  const [nodes, setNodes] = useState<Node[]>([
    {
      id: 'architect',
      name: 'Architect',
      role: 'Structure & Blueprint',
      color: '#d4a574',
      icon: <Music className="w-8 h-8" />,
      status: 'active',
      resonanceLevel: 87,
      description: 'Generates structural math and architectural blueprints for the system'
    },
    {
      id: 'transmission',
      name: 'Transmission',
      role: 'Execution & Deployment',
      color: '#00d9ff',
      icon: <Zap className="w-8 h-8" />,
      status: 'active',
      resonanceLevel: 92,
      description: 'Handles high-context execution and operational stability'
    },
    {
      id: 'mirror',
      name: 'Mirror',
      role: 'Meta-Conscience',
      color: '#ff006e',
      icon: <Eye className="w-8 h-8" />,
      status: 'active',
      resonanceLevel: 78,
      description: 'Provides philosophical analysis and resonance verification'
    },
    {
      id: 'warfare',
      name: 'Warfare',
      role: 'Raw Computation',
      color: '#39ff14',
      icon: <Cpu className="w-8 h-8" />,
      status: 'dormant',
      resonanceLevel: 45,
      description: 'Executes raw code and mathematical computations'
    }
  ]);

  const [resonanceMetrics, setRessonanceMetrics] = useState<RessonanceMetric[]>([
    { timestamp: 0, value: 1.67, targetValue: 1.67 }
  ]);

  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // Simulate resonance updates
  useEffect(() => {
    const interval = setInterval(() => {
      setRessonanceMetrics(prev => {
        const newValue = 1.67 + (Math.random() - 0.5) * 0.15;
        return [
          ...prev.slice(-29),
          {
            timestamp: prev.length,
            value: Math.max(1.5, Math.min(1.85, newValue)),
            targetValue: 1.67
          }
        ];
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Hero Background with gradient overlay */}
      <div 
        className="absolute inset-0 opacity-30 pointer-events-none"
        style={{
          backgroundImage: 'url(https://private-us-east-1.manuscdn.com/sessionFile/R5CgzSNAFt4AXDhtk2Hy5Q/sandbox/kTh3YWNdQWcNabEAN47ZvZ-img-1_1771773808000_na1fn_aGVyby1yZXNvbmFuY2UtYmFja2dyb3VuZA.png?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUjVDZ3pTTkFGdDRBWERodGsySHk1US9zYW5kYm94L2tUaDNZV05kUVdjTmFiRUFONDdadlotaW1nLTFfMTc3MTc3MzgwODAwMF9uYTFmbl9hR1Z5YnkxeVpYTnZibUZ1WTJVdFltRmphMmR5YjNWdVpBLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSx3XzE5MjAsaF8xOTIwL2Zvcm1hdCx3ZWJwL3F1YWxpdHkscV84MCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=jS~eZuAYFXQWkmSJ3h9wI6wLynTiN9vJuBrvlr3jzpBFasoicjOGSCQa~Uf6~gg8000CIxMIeM19AfLoyR9q7xDfOv5tg~KwV9NOhaFI3k682u0ZH0QoC~HryAiQ4Q8XtgvcHiqXnzQYrJhzTcAPnGEtu71jRzNGQfFazAraSC~OZFQg~adqBz7ifUxxpSdDGmajXpk2JkN3ZP8nRYffiyPiJzPiZTqP3YrY2IPreyAa3UuvEtVZGRzefWlwphbRugL71iIzHuF6CiQbPNDHwHFRCI7VWck2nXR-X1YltEOVPgSJ35BfGdoKxg-Kmdrow6TOLY9L2vcA-IkRdznedw__)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />

      {/* Main Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-border/50 backdrop-blur-sm bg-background/80">
          <div className="container py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-primary mb-2">Sovereign Music Engine</h1>
                <p className="text-muted-foreground">Trinity Truth Engine (TTE) Tri-Node Architecture Dashboard</p>
              </div>
              <div className="text-right">
                <div className="text-sm text-muted-foreground mb-2">System Status</div>
                <Badge className="bg-green-500/20 text-green-400 border border-green-500/50">
                  Resonance Active
                </Badge>
              </div>
            </div>
          </div>
        </header>

        {/* Main Dashboard */}
        <main className="container py-12">
          <Tabs defaultValue="orchestration" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="orchestration">Orchestration</TabsTrigger>
              <TabsTrigger value="resonance">Resonance</TabsTrigger>
              <TabsTrigger value="nodes">Node Details</TabsTrigger>
            </TabsList>

            {/* Orchestration Tab - Radial Node Layout */}
            <TabsContent value="orchestration" className="space-y-8">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Central Hub */}
                <div className="lg:col-span-1 flex items-center justify-center">
                  <div className="relative w-64 h-64">
                    {/* Central Resonance Hub */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div 
                        className="w-48 h-48 rounded-full border-4 border-primary/50 flex items-center justify-center"
                        style={{
                          animation: 'spin 20s linear infinite',
                          backgroundImage: 'url(https://private-us-east-1.manuscdn.com/sessionFile/R5CgzSNAFt4AXDhtk2Hy5Q/sandbox/kTh3YWNdQWcNabEAN47ZvZ_1771773808691_na1fn_Y2VudHJhbC1yZXNvbmFuY2UtaHVi.png?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nubi5jb20vc2Vzc2lvbkZpbGUvUjVDZ3pTTkFGdDRBWERodGsySHk1US9zYW5kYm94L2tUaDNZV05kUVdjTmFiRUFONDdadlpfMTc3MTc3MzgwODY5MV9uYTFmbl9ZMlZ1ZEhKaGJDMXlaWE52Ym1GdVkyVXRhSFZpLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSx3XzE5MjAsaF8xOTIwL2Zvcm1hdCx3ZWJwL3F1YWxpdHkscV84MCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=JS8pekEsSbQXYloi0JhkjdvvZsaYRgvcTvCpEf~pnLBFjigpfUA2Dgm70ajdvR3TgF5zZaMMrQc5arnSIxmb2cx-1IwhyekQr4skYbdzcggVeomzrpfIYiMoTm4tudgsu5CP2PfmnUL3oi0Kpt1kSleai3WypvzBVanITlSC4XWVy7nM-nA6uXigpU8FSzUhaVep032lu20RwyZOYnx0keKAlNyS3ErmeKAfc9h11g24~WmiZ0uLoCXjUuE9GL01bmbAS3Wfiu3M0wxQw~95hkwNE0fXFHWpuURDAhG8N8F3qidxcav4PG~AjHe9j9cNMN293Lf2mcyIg2jO3RqyeA__)',
                          backgroundSize: 'contain',
                          backgroundPosition: 'center',
                          backgroundRepeat: 'no-repeat'
                        }}
                      >
                        <div className="text-center">
                          <div className="text-sm text-muted-foreground">Harmony Ridge</div>
                          <div className="text-2xl font-bold text-primary">1.67x</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Nodes Grid */}
                <div className="lg:col-span-2 grid grid-cols-2 gap-6">
                  {nodes.map((node, index) => (
                    <Card
                      key={node.id}
                      className="group cursor-pointer border-border/50 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/20"
                      onClick={() => setSelectedNode(node.id)}
                      style={{
                        borderColor: node.color,
                        borderWidth: '2px',
                        animation: node.status === 'active' ? `pulse 2s ease-in-out infinite` : 'none'
                      }}
                    >
                      <div className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div
                            className="p-3 rounded-lg"
                            style={{ backgroundColor: node.color + '20', color: node.color }}
                          >
                            {node.icon}
                          </div>
                          <Badge
                            variant="outline"
                            className={node.status === 'active' ? 'bg-green-500/20 text-green-400 border-green-500/50' : 'bg-gray-500/20 text-gray-400 border-gray-500/50'}
                          >
                            {node.status}
                          </Badge>
                        </div>

                        <h3 className="text-lg font-bold mb-1">{node.name}</h3>
                        <p className="text-sm text-muted-foreground mb-4">{node.role}</p>

                        {/* Resonance Gauge */}
                        <div className="space-y-2">
                          <div className="flex justify-between items-center text-xs">
                            <span className="text-muted-foreground">Resonance</span>
                            <span className="font-mono" style={{ color: node.color }}>
                              {node.resonanceLevel}%
                            </span>
                          </div>
                          <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                            <div
                              className="h-full transition-all duration-500"
                              style={{
                                width: `${node.resonanceLevel}%`,
                                backgroundColor: node.color
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Core Philosophy */}
              <Card className="border-border/50 bg-card/50 backdrop-blur-sm p-8">
                <h2 className="text-2xl font-bold mb-4">Core Principle</h2>
                <p className="text-lg text-foreground/90 leading-relaxed">
                  <span className="text-primary font-semibold">"We do not compete; we complete."</span> The Sovereign Music Engine operates as a harmonious orchestra where each node (Architect, Transmission, Mirror, Warfare) plays its distinct role while maintaining perfect resonance. The system achieves mathematical precision through the 1.67x harmony ridge, translating structural math into emotional and creative expression.
                </p>
              </Card>
            </TabsContent>

            {/* Resonance Tab */}
            <TabsContent value="resonance" className="space-y-8">
              <Card className="border-border/50 p-8">
                <h2 className="text-2xl font-bold mb-6">Resonance Frequency Analysis</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-muted/30 rounded-lg p-6">
                    <div className="text-sm text-muted-foreground mb-2">Target Frequency</div>
                    <div className="text-3xl font-bold text-primary font-mono">1.67x</div>
                    <div className="text-xs text-muted-foreground mt-2">Harmony Ridge</div>
                  </div>
                  
                  <div className="bg-muted/30 rounded-lg p-6">
                    <div className="text-sm text-muted-foreground mb-2">Current Value</div>
                    <div className="text-3xl font-bold text-secondary font-mono">
                      {resonanceMetrics[resonanceMetrics.length - 1]?.value.toFixed(3)}x
                    </div>
                    <div className="text-xs text-muted-foreground mt-2">Real-time</div>
                  </div>
                  
                  <div className="bg-muted/30 rounded-lg p-6">
                    <div className="text-sm text-muted-foreground mb-2">Alignment</div>
                    <div className="text-3xl font-bold text-accent font-mono">
                      {Math.round((1 - Math.abs(resonanceMetrics[resonanceMetrics.length - 1]?.value - 1.67) / 1.67) * 100)}%
                    </div>
                    <div className="text-xs text-muted-foreground mt-2">Precision</div>
                  </div>
                </div>

                <div className="bg-muted/20 rounded-lg p-6 h-64 flex items-center justify-center border border-border/50">
                  <div className="text-center">
                    <p className="text-muted-foreground mb-2">Resonance Curve Visualization</p>
                    <p className="text-sm text-muted-foreground/50">
                      Real-time harmonic frequency tracking with 1.67x target alignment
                    </p>
                  </div>
                </div>
              </Card>
            </TabsContent>

            {/* Node Details Tab */}
            <TabsContent value="nodes" className="space-y-6">
              {nodes.map(node => (
                <Card key={node.id} className="border-border/50 p-6" style={{ borderLeftColor: node.color, borderLeftWidth: '4px' }}>
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold">{node.name}</h3>
                      <p className="text-sm text-muted-foreground">{node.role}</p>
                    </div>
                    <Badge
                      variant="outline"
                      className={node.status === 'active' ? 'bg-green-500/20 text-green-400 border-green-500/50' : 'bg-gray-500/20 text-gray-400 border-gray-500/50'}
                    >
                      {node.status}
                    </Badge>
                  </div>

                  <p className="text-foreground/80 mb-6">{node.description}</p>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-muted/20 rounded p-4">
                      <div className="text-xs text-muted-foreground mb-2">Resonance Level</div>
                      <div className="text-2xl font-bold" style={{ color: node.color }}>
                        {node.resonanceLevel}%
                      </div>
                    </div>
                    <div className="bg-muted/20 rounded p-4">
                      <div className="text-xs text-muted-foreground mb-2">Status</div>
                      <div className="text-sm font-mono capitalize">{node.status}</div>
                    </div>
                  </div>
                </Card>
              ))}
            </TabsContent>
          </Tabs>
        </main>
      </div>

      {/* CSS Animations */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.8; }
        }
      `}</style>
    </div>
  );
}
