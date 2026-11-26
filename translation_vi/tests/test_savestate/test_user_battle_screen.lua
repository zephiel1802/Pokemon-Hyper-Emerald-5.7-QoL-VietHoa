local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local A_KEY = 1

callbacks:add('frame', function()
    f = f + 1
    
    if f == 5 then
        emu:screenshot(DIR .. 'user_battle_frame_05.png')
    end
    
    -- Press A button periodically to advance message
    if (f % 20) < 5 then
        emu:setKeys(A_KEY)
    else
        emu:setKeys(0)
    end
    
    if f == 30 then emu:screenshot(DIR .. 'user_battle_frame_30.png') end
    if f == 60 then emu:screenshot(DIR .. 'user_battle_frame_60.png') end
    if f == 90 then emu:screenshot(DIR .. 'user_battle_frame_90.png') end
    if f == 120 then emu:screenshot(DIR .. 'user_battle_frame_120.png') end
    if f == 180 then emu:screenshot(DIR .. 'user_battle_frame_180.png') end
    if f == 240 then
        emu:screenshot(DIR .. 'user_battle_frame_240.png')
        local fh = io.open(DIR .. 'user_battle_done.txt', 'w')
        fh:write('done')
        fh:close()
    end
end)
