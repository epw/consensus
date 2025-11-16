FORMAT_REGEX = '(html|epub).*'

local function pagereflink(format, link, before, after)
  if format:match 'latex' then
    return pandoc.RawInline('latex', before .. link .. ' (page \\pageref{' .. link .. '})' .. after)
  elseif format:match FORMAT_REGEX then
    link_href = string.lower(link)
    link_href = string.gsub(link_href, "%s+", "_")
    return pandoc.RawInline('html',before .. '<a href="#' .. link_href .. '">' .. link .. '</a>' .. after)
  else
    return pandoc.Str("Whoops")
  end
end

local function pagerefanchor(format, anchor, before, after)
  if format:match 'latex' then
    return pandoc.RawInline('latex', before ..'\\label{' .. anchor .. '}' .. after)
  elseif format:match FORMAT_REGEX then
    anchor_id = string.lower(anchor)
    anchor_id = string.gsub(anchor_id, "%s+", "_")
    return pandoc.RawInline('html', before .. '<a id="' .. anchor_id .. '"></a>' .. after)
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
