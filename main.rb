  require 'selenium-webdriver'
  require 'dotenv/load'
  require 'json'

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

  headers = {
    "Authorization" => "Bearer #{ENV['GITHUB_TOKEN']}",
    "X-GitHub-Api-Version" => "2022-11-28",
    "User-Agent" => "pronoun_scraping_app"
  }

  # Configurar e fazer get de uma página de contribuidores
  response = Net::HTTP.get(URI("#{ENV['GITHUB_API_URL']}repos/JabRef/jabref/contributors?page=1&per_page=100"))
  data = JSON.parse(response)

  # File.write(path, JSON.dump(data))

  # Realizar login com credenciais em .env
  puts "---------- Fazendo login ----------"
  scraper.get "#{github_url+'login'}"

  username_input = scraper.find_element(:id, 'login_field')
  password_input = scraper.find_element(:id, 'password')

  username_input.send_keys(ENV['USERNAME'])
  password_input.send_keys(ENV['PASSWORD'])

  login_button = scraper.find_element(:name, 'commit')
  login_button.click

  stats = [0,0,0]

  data.each do |contributor|
    puts "\n\n\n------------------"
    
    begin
      scraper.get "#{github_url+contributor['login']}"

      pronouns = wait.until { scraper.find_element(:css, '[itemprop="pronouns"]') }.text

      puts "#{contributor['login']} - #{pronouns}"

      if pronouns == 'she/her'
        stats[0] += 1
      else
        stats[1] += 1
      end
    rescue 
      puts "#{contributor['login']} - no pronouns in bio"
      stats[2] += 1
    end
    
    puts "------------------\n\n\n"
  end

  puts "------------------"
  puts stats[0]
  puts stats[1]
  puts stats[2]
  puts "------------------"

  puts "---------- Fim ----------"