def gen_string(n)
	s = ""	
	chars = ['A', 'T', 'C', 'G']	
	for i in 0...n
		t = rand(4)
		s = s << chars[t].to_s
	end
	s.to_s
end

#for i in 1...100
#	s1 = gen_string(i * 10)
#	s2 = gen_string(i * 10)
#	t = `ruby-prof msa.rb #{s1} #{s2}`
#	puts i.to_s << "," << t.split("\n").last.split()[1]
#end

for i in 1...100
	s1 = gen_string(i * 10)
	s2 = gen_string(i * 10)
	t = `python test.py #{s1} #{s2}`
	puts i.to_s << "," << t.split("\n").first.split()[4]
end
