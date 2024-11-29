require 'json'

users_list = JSON.parse(File.read('./users.json'))
stats = Hash.new(0)

users_list.each do |user|
  user_data = JSON.parse(File.read("./users/#{user['login']}.json"))
  stats["#{user_data['pronouns']}"] += 1
end

puts "\n---Dados brutos---"
stats.each do |chave, valor|
  puts "#{chave} - #{valor}"
end
puts "------------------\n"

puts "\n----Dados em %----"
stats.each do |chave, valor|
  puts "#{chave} - #{(valor.to_f / users_list.length * 100).round(2)}%"
end
puts "------------------\n"