local i = 0
for _, surface in pairs(game.surfaces) do
    for _, inserter in pairs(surface.find_entities_filtered{type='inserter'}) do
        if not string.match(inserter.name, "filter") then
            inserter.inserter_filter_mode = 'blacklist'
        end
    end

    for _, inserter in pairs(surface.find_entities_filtered{type='inserter', name={'filter-inserter', 'stack-filter-inserter'}}) do
        local inserter_mode = inserter.inserter_filter_mode
        local replacement = surface.create_entity{
            name = inserter.name == 'filter-inserter' and 'fast-inserter' or 'stack-inserter',
            position = inserter.position,
            direction = inserter.direction,
            force = inserter.force,
            raise_built = true,
            create_build_effect_smoke = false
        }
        if replacement.valid then
            for _, wire in pairs(inserter.circuit_connection_definitions) do
                replacement.connect_neighbour(wire)
            end
            replacement.copy_settings(inserter)
            replacement.inserter_filter_mode = inserter_mode
            inserter.destroy()
            i = i + 1
        else
            game.print('Failed to migrate inserter at '..serpent.line(inserter.position))
        end
    end
end
game.print('Migrated '..i..' filter inserters.')