local looking_at_playbook = false
local playbook = {}

function Block (elem)
  if looking_at_playbook then
    playbook[#playbook + 1] = elem
    return elem
  end
end

function Header (elem)
  if elem.level == 1 and elem.identifier == 'the-characters' then
    looking_at_playbook = true
    return elem
  else
    looking_at_playbook = looking_at_playbook and elem.level ~= 1
  end
end
