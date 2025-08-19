# JAMA Abstract MCP

Bu MCP (Model Context Protocol) servisi, JAMA Network makalelerinden görsel özet içeren PowerPoint dosyaları oluşturur.

## Özellikler

- **scrape_jama_article**: JAMA Network makale URL'sinden makale verilerini çeker
- **create_powerpoint**: Çekilen veriyi kullanarak görsel özet PowerPoint dosyası oluşturur
- İsteğe bağlı GitHub release'e yükleme desteği

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### 1. Veri Çekme

```python
# JAMA makalesinden veri çek
result = await scrape_jama_article("https://jamanetwork.com/journals/jama/fullarticle/...")
data = result["data"]
```

### 2. PowerPoint Oluşturma

```python
# PowerPoint dosyası oluştur
result = await create_powerpoint(
    data=data,
    output_filename="my_abstract.pptx"
)
```

### 3. GitHub'a Yükleme (Opsiyonel)

```python
# GitHub release'e yükle
result = await create_powerpoint(
    data=data,
    github_repo="kullanici/repoadi",
    github_token="ghp_..."
)
```

## Çevre Değişkenleri

- `JAMA_TEMPLATE`: PowerPoint template dosyası yolu (varsayılan: `templates/abstract.pptx`)
- `OUTPUT_DIR`: Çıktı dosyaları dizini (varsayılan: `outputs`)

## Template Gereksinimleri

PowerPoint template dosyası aşağıdaki shape'lere sahip olmalıdır:

- `title`: Makale başlığı
- `footer_citation`: URL referansı
- `population_subtitle`: Katılımcı alt başlığı
- `population_description`: Katılımcı açıklaması
- `intervention_subtitle`: Müdahale alt başlığı
- `intervention_description`: Müdahale açıklaması
- `settings_locations_description`: Ayar ve konum bilgileri
- `primary_outcome_description`: Birincil sonuç
- `findings_description_1`: Bulgular açıklaması 1
- `findings_description_2`: Bulgular açıklaması 2

## Smithery Deployment

Bu MCP servisi Smithery'de deploy edilmeye hazırdır. İki ana tool sağlar:

1. **scrape_jama_article**: Makale verilerini çeker
2. **create_powerpoint**: PowerPoint dosyası oluşturur ve opsiyonel olarak GitHub'a yükler
