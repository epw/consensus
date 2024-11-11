local function voiced_open(format, el)
   voice = el.text:match("{(%a+)}")
   return pandoc.RawBlock(format, "<div class='voice voice-" .. voice .. "'>")
end

local function voiced_close(format)
   return pandoc.RawBlock(format, "</div>")
end

local function is_voice_begin(block)
  return block:match '^\\Begin'
end

local function is_voice_end(block)
  return block:match '^\\End'
end

-- Filter function called on each RawBlock element.
function RawBlock (el)
  -- Only output specially for HTML
  if not FORMAT:match 'html.*' then
    return nil
  end
  if is_voice_begin(el.text) then
     return voiced_open(FORMAT, el)
  end
  if is_voice_end(el.text) then
     return voiced_close(FORMAT, el)
  end
  -- otherwise, leave the block unchanged
  return nil
end

return {
  {RawBlock = RawBlock}
}
