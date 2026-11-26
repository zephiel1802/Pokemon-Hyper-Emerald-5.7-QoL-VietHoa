local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'direct_script_exec.log', 'w')
local f = 0
local A_KEY = 1

callbacks:add('frame', function()
  f = f + 1

  -- At frame 5: force launch script 0x098536A1
  if f == 5 then
    -- Clear stack and set script ptr
    emu:write8(0x03000EB0, 0) -- stackDepth
    emu:write32(0x03000EB8, 0x098536A1) -- scriptPtr
    emu:write8(0x03000EB1, 1) -- mode: SCRIPT_MODE_BYTECODE
    log:write("Injected script 0x098536A1 into sScriptContext1 at frame 5\n")
  end

  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr  = emu:read32(0x03000EB8)
  local cb2 = emu:read32(0x030022C4)

  -- Mash A every few frames to advance dialogs
  if f >= 10 then
    if (f % 16) < 4 then
      emu:setKeys(A_KEY)
    else
      emu:setKeys(0)
    end
  end

  if f <= 30 or f % 15 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d cb2=%08X sc1=(mode:%d, ptr:%08X)\n",
      f, cb2, sc1_mode, sc1_ptr))
  end

  -- Take screenshots around interesting frames
  if f == 15 then emu:screenshot(DIR .. 'direct_f015.png') end
  if f == 40 then emu:screenshot(DIR .. 'direct_f040.png') end
  if f == 80 then emu:screenshot(DIR .. 'direct_f080.png') end
  if f == 120 then emu:screenshot(DIR .. 'direct_f120.png') end
  if f == 160 then emu:screenshot(DIR .. 'direct_f160.png') end
  if f == 200 then emu:screenshot(DIR .. 'direct_f200.png') end
  if f == 250 then emu:screenshot(DIR .. 'direct_f250.png') end
  if f == 300 then emu:screenshot(DIR .. 'direct_f300.png') end
  if f == 400 then emu:screenshot(DIR .. 'direct_f400.png') end

  if f >= 450 then
    log:close()
    local fh = io.open(DIR .. 'direct_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)
