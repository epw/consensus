local function pagereflink(format, link, before, after)
  if format:match 'latex' then
    return pandoc.RawInline('latex', before .. link .. ' (page \\pageref{' .. link .. '})' .. after)
  elseif format:match 'html.*' then
    return pandoc.RawInline('html',before .. '<a href=#' .. link .. '>' .. link .. '</a>' .. after)
  else
    return pandoc.Str("Whoops")
  end
end

local function pagerefanchor(format, anchor, before, after)
  if format:match 'latex' then
    return pandoc.RawInline('latex', before ..'\\label{' .. anchor .. '}' .. after)
  elseif format:match 'html.*' then
    return pandoc.RawInline('html', before .. '<a id="' .. anchor .. '"></a>' .. after)
  else
    return pandoc.Str("Whoops")
  end
end

return {
  {
  Para = function (elem)
    elemstr = pandoc.utils.stringify(elem)
    if elemstr:match ".*{{link.*}}.*" then
		link = (elemstr:match ".*{{link(.*)}}.*")
		before = (elemstr:match "(.*){{link.*}}.*")
		after = (elemstr:match ".*{{link.*}}(.*)")
		return pandoc.Para(pagereflink(FORMAT, link, before, after))
	elseif elemstr:match ".*{{anchor.*}}.*" then
		anchor = (elemstr:match ".*{{anchor(.*)}}.*")
		before = (elemstr:match "(.*){{anchor.*}}.*")
		after = (elemstr:match ".*{{anchor.*}}(.*)")
	  return pandoc.Para(pagerefanchor(FORMAT, anchor, before, after))
    else
      return elem
    end
  end,
  }
}