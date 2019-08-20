local function itemreplace(format)
   if format:match 'latex' then
     return pandoc.RawInline('\\item')
   elseif format:match 'html.*' then
     return pandoc.RawInline('<li>')
   else
     return pandoc.Str("Whoops")
   end
end

local function beginreplace(format)
   if format:match 'latex' then
     return pandoc.RawInline('\\begin{itemize*}')
   elseif format:match 'html.*' then
     return pandoc.RawInline('<ul>')
   else
     return pandoc.Str("Whoops")
   end
end

local function endreplace(format)
   if format:match 'latex' then
     return pandoc.RawInline('\\end{itemize*}')
   elseif format:match 'html.*' then
     return pandoc.RawInline('<ul>')
   else
     return pandoc.Str("Whoops")
   end
end

return {
  {
  Para = function (elem)
    elemstr = pandoc.utils.stringify(elem)
    if elemstr:match ".*\item.*" then
		return pandoc.Para(itemreplace(FORMAT))
    if elemstr:match ".*\begin{itemize\*}.*" then
		return pandoc.Para(beginreplace(FORMAT))
    if elemstr:match ".*\end{itemize\*}.*" then
		return pandoc.Para(endreplace(FORMAT))
    else
      return elem
    end
  end,
  }
}
