FORMAT_REGEX = '(html|epub).*'

local function itemreplace(format)
   if format:match 'latex' then
     return '\\item'
   elseif format:match FORMAT_REGEX then
      return pandoc.RawBlock(FORMAT_REGEX, '<li>')
   else
     return "Whoops"
   end
end

local function beginreplace(format)
   if format:match 'latex' then
     return '\\begin{itemize*}'
   elseif format:match FORMAT_REGEX then
     return pandoc.RawBlock(FORMAT_REGEX, '<ul>')
   else
     return "Whoops"
   end
end

local function endreplace(format)
   if format:match 'latex' then
     return '\\end{itemize*}'
   elseif format:match FORMAT_REGEX then
     return pandoc.RawBlock(FORMAT_REGEX, '</ul>')
   else
     return "Whoops"
   end
end

return {
  {
  Inline = function (elem)
    elemstr = pandoc.utils.stringify(elem)
    if elemstr:match "{{item}}" then
		return itemreplace(FORMAT)
    elseif elemstr:match "{{begininline}}" then
		return beginreplace(FORMAT)
    elseif elemstr:match "{{endinline}}" then
		print (elemstr)
		return endreplace(FORMAT)
    else
      return elem
    end
  end,
  }
}
