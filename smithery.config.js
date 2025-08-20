// Smithery configuration for JAMA Abstract Generator MCP Server
const config = {
  name: "jama-abstract-generator",
  description: "JAMA Network makale URL'sinden görsel özet içeren PowerPoint dosyası oluşturan MCP server",
  
  // Server configuration
  server: {
    command: "python",
    args: ["-m", "server"],
    env: {
      PYTHONPATH: ".",
      PYTHONUNBUFFERED: "1",
      JAMA_TEMPLATE: "templates/abstract.pptx",
      OUTPUT_DIR: "outputs"
    }
  },

  // MCP tools configuration
  tools: [
    {
      name: "scrape_jama_article",
      description: "Bir JAMA Network Open makale URL'sinden makale verilerini çeker ve yapılandırılmış formatta döndürür.",
      inputSchema: {
        type: "object",
        properties: {
          url: {
            type: "string",
            description: "Veri çekilecek JAMA Network makalesinin tam URL'si",
            pattern: "^https://jamanetwork\\.com/.*"
          }
        },
        required: ["url"]
      },
      outputSchema: {
        type: "object",
        properties: {
          result: {
            type: "string",
            description: "İşlem sonucu mesajı"
          },
          data: {
            type: "object",
            description: "Çekilen makale verileri"
          }
        }
      }
    },
    {
      name: "create_powerpoint",
      description: "Çekilen makale verilerini kullanarak görsel özet içeren bir PowerPoint (PPTX) dosyası oluşturur.",
      inputSchema: {
        type: "object",
        properties: {
          data: {
            type: "object",
            description: "scrape_jama_article tool'undan dönen veri objesi"
          },
          output_filename: {
            type: "string",
            description: "Çıktı dosyasının adı (opsiyonel, varsayılan: visual_abstract.pptx)"
          },
          github_repo: {
            type: "string",
            description: "Yükleme yapılacak GitHub reposu. Biçim: kullanici/repoadi (opsiyonel)"
          },
          github_token: {
            type: "string",
            description: "Repoya yazma izni olan Personal Access Token (opsiyonel)"
          }
        },
        required: ["data"]
      },
      outputSchema: {
        type: "object",
        properties: {
          result: {
            type: "string",
            description: "İşlem özeti (başarılı/başarısız mesajı)"
          },
          output_path: {
            type: "string",
            description: "Yerelde oluşturulan PPTX yolu"
          },
          download_url: {
            type: "string",
            description: "Release'e yüklendiyse herkese açık indirme linki"
          }
        }
      }
    }
  ],

  // Build configuration
  build: {
    dockerfile: "Dockerfile",
    context: ".",
    target: "latest"
  },

  // Runtime configuration
  runtime: {
    env: {
      PYTHONPATH: "/app",
      PYTHONUNBUFFERED: "1",
      JAMA_TEMPLATE: "templates/abstract.pptx",
      OUTPUT_DIR: "outputs"
    }
  },

  // Health check configuration
  health: {
    path: "/health",
    port: 8000,
    initialDelay: 30,
    period: 10,
    timeout: 5,
    failureThreshold: 3
  },

  // Resource limits
  resources: {
    cpu: "0.5",
    memory: "512Mi",
    storage: "1Gi"
  },

  // Scaling configuration
  scaling: {
    minReplicas: 1,
    maxReplicas: 3,
    targetCpuUtilization: 70
  },

  // Networking
  networking: {
    ports: [
      {
        port: 8000,
        protocol: "TCP",
        name: "http"
      }
    ]
  },

  // Volumes for persistent storage
  volumes: [
    {
      name: "outputs",
      mountPath: "/app/outputs",
      size: "1Gi"
    },
    {
      name: "templates",
      mountPath: "/app/templates",
      size: "100Mi"
    }
  ]
};

module.exports = config;
