  require 'selenium-webdriver'
  require 'dotenv/load'

  puts "---------- Iniciando Script ----------"
  
  Dotenv.overload
  
  # Configurando webdriver
  client = Selenium::WebDriver::Remote::Http::Default.new
  options = Selenium::WebDriver::Chrome::Options.new
  options.add_argument('--headless')
  scraper = Selenium::WebDriver.for(:chrome, options: options, http_client: client)
  
  # Arquivo para guardar dados
  path = 'C:\Users\Maria Fernanda\Desktop\TCC 2\github_pronoun_scraper\users.json'
  File.open(path, 'w')

  wait = Selenium::WebDriver::Wait.new(timeout: 10)

  # Definir url
  github_url = ENV['GITHUB_URL']

  # Configurando acesso a API do GitHub
  # Configurando o cabeçalho de autenticação

  headers = {
    "Authorization" => "Bearer #{ENV['GITHUB_TOKEN']}",
    "X-GitHub-Api-Version" => "2022-11-28",
    "User-Agent" => "pronoun_scraping_app"
  }

  # Configurar e fazer get de um usuário
  # response = Net::HTTP.get(URI("#{ENV['GITHUB_API_URL']}users/MariaPinguelli"))
  # data = JSON.parse(response)

  # Realizar login com credenciais em .env
  puts "---------- Fazendo login ----------"
  # scraper.get "#{github_url+'login'}"

  # username_input = scraper.find_element(:id, 'login_field')
  # password_input = scraper.find_element(:id, 'password')

  # username_input.send_keys(ENV['USERNAME'])
  # password_input.send_keys(ENV['PASSWORD'])

  # login_button = scraper.find_element(:name, 'commit')
  # login_button.click

  # Acessar repositório
  puts "---------- Buscando lista de colaboradores ----------"
  repo_namespace = 'JabRef/jabref' #Formato owner/repo

  uri = URI("#{ENV['GITHUB_API_URL']}repos/#{repo_namespace}/collaborators")
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: true) do |http|
    request = Net::HTTP::Get.new(uri, headers)
    http.request(request)
  end

  if response.is_a?(Net::HTTPSuccess)
    contributors = JSON.parse(response)
    puts "\n\n\n------------------"
    puts contributors
    puts "------------------\n\n\n"
  else
    puts "Erro: #{response.code} - #{response.message} --- #{response.body}"
  end
  
  # scraper.get "#{github_url+data["login"]}"

  # pronouns = wait.until { scraper.find_element(:css, '[itemprop="pronouns"]') }.text

  # puts "\n\n\n------------------"
  # puts pronouns
  # puts "------------------\n\n\n"

  puts "---------- Fim ----------"