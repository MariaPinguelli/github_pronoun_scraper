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

  # Configurar e fazer get de um usuário
  response = Net::HTTP.get(URI("#{ENV['GITHUB_API_URL']}users/MariaPinguelli"))
  data = JSON.parse(response)

  puts "\n\n\n------------------"
  puts data["login"]
  puts "------------------\n\n\n"

  # Navegar para a página desejada
  scraper.get "#{github_url+'login'}"

  username_input = scraper.find_element(:id, 'login_field')
  password_input = scraper.find_element(:id, 'password')

  username_input.send_keys(ENV['USERNAME'])
  password_input.send_keys(ENV['PASSWORD'])

  puts "---------- Fazendo login ----------"
  login_button = scraper.find_element(:name, 'commit')
  login_button.click

  scraper.get "#{github_url+data["login"]}"

  pronouns = wait.until { scraper.find_element(:css, '[itemprop="pronouns"]') }.text

  puts "\n\n\n------------------"
  puts pronouns
  puts "------------------\n\n\n"

  puts "---------- Fim ----------"