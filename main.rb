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

wait = Selenium::WebDriver::Wait.new(timeout: 3)
wait_login = Selenium::WebDriver::Wait.new(timeout: 35)

# Configurando acesso a API do GitHub
github_url = ENV['GITHUB_URL']

headers = {
  "Authorization" => "Bearer #{ENV['GITHUB_TOKEN']}",
  "X-GitHub-Api-Version" => "2022-11-28",
  "User-Agent" => "pronoun_scraping_app"
}

# Arquivo para guardar dados
users_file = './users.json'
saved_users = []

begin
  File.open(users_file, 'r')
rescue Errno::ENOENT => e
  puts "File not found: #{e.message}"
  puts "Creating file"
  File.open(users_file, 'w')
end

file_content = File.read(users_file)
saved_users = JSON.parse(file_content) unless file_content.empty?
data = []
contributors = []
i = 0

begin
  i += 1
  response = Net::HTTP.get(
    URI("#{ENV['GITHUB_API_URL']}repos/JabRef/jabref/contributors?page=#{i}&per_page=100"),
    headers
  )
  data = JSON.parse(response)
  data.each do |contributor|
    unless saved_users.any? { |user| user['login'] == contributor['login'] } || contributor['login'].include?('[bot]') 
      contributors << contributor
    end
  end
end while !data.empty?

unless contributors.empty?
  saved_users.concat(contributors)
  File.write(users_file, JSON.pretty_generate(saved_users))
  puts "before scraper.get"
  #Login
  scraper.get "#{github_url+'login'}"

  username_input = scraper.find_element(:id, 'login_field')
  password_input = scraper.find_element(:id, 'password')
  
  username_input.send_keys(ENV['USERNAME'])
  password_input.send_keys(ENV['PASSWORD'])
  puts 'input data'

  login_button = scraper.find_element(:name, 'commit')
  login_button.click
  puts 'clicked'

  sleep(30)

  contributors.each do |contributor|
    file_path = "./users/#{contributor['login']}.json"
    
    begin
      File.open(file_path, 'r')
    rescue Errno::ENOENT => e
      # puts "File not found: #{e.message}"
      # puts "Creating file"

      File.open(file_path, 'w')

      response = Net::HTTP.get(
        URI("#{ENV['GITHUB_API_URL']}users/#{contributor['login']}"),
        headers
      )
      user = JSON.parse(response)

      scraper.get "#{github_url+contributor['login']}"

      begin
        pronouns = wait.until { scraper.find_element(:css, '[itemprop="pronouns"]') }.text
        user['pronouns'] = pronouns
        puts pronouns
      rescue => e
        puts "\n\nERRO #{e}\n\n"
        user['pronouns'] = 'no_pronouns'
      end

      File.write(file_path, JSON.pretty_generate(user))
    end

  end
else
  puts "Não existem novos contribuidores a serem adicionados ao banco de dados."
end

scraper.quit