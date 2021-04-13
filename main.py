class BackpackTaskSolveAlgorithm:
    def __init__(self, backpack_capacity, volume_map, price_map):
        self.__backpack_capacity = backpack_capacity
        self.__volume_map = volume_map
        self.__price_map = price_map

    def solve(self, last_item_index=0, last_interval_map=None):
        interval_map = self.__get_interval_map(last_item_index, last_interval_map)
        if len(self.__volume_map) <= last_item_index + 1:
            return interval_map[self.__backpack_capacity]

        return self.solve(last_item_index + 1, interval_map)

    def __print(self, volume_messages):
        for index in range(0, len(volume_messages)):
            messages_info = volume_messages[index]
            if index + 1 != len(volume_messages):
                next_volume = volume_messages[index + 1][0] - 1
            else:
                next_volume = self.__backpack_capacity
            print('For ' + str(messages_info[0]) + '-' + str(next_volume) + ':')
            for key in range(0, len(messages_info[2])):
                message = messages_info[2][key]
                print(message)

    def __get_interval_map(self, item_index, last_interval_map=None):
        if last_interval_map is None:
            interval_map = {}
        else:
            interval_map = last_interval_map

        messages = []
        for volume in range(0, self.__backpack_capacity + 1):
            max_item_count = volume // self.__volume_map[item_index]

            if volume not in interval_map:
                item_price = max_item_count * self.__price_map[item_index]
                interval_map[volume] = [item_price, {item_index: max_item_count}]

                if volume not in messages:
                    messages.append([volume, item_price, []])

                if volume == 0 or messages[-2][1] != item_price:
                    messages[-1][2].append('f' + str(item_index) + '(' + str(volume) + ') = ' + str(item_price))
                elif volume != messages[-2][0]:
                    messages.pop()

            else:
                item_count = 0
                max_price = last_interval_map[volume][0]
                for count in range(0, max_item_count + 1):
                    item_volume = count * self.__volume_map[item_index]
                    item_price = count * self.__price_map[item_index]
                    general_price = last_interval_map[volume - item_volume][0] + item_price
                    item_count_map = last_interval_map[volume - count * self.__volume_map[item_index]][1].copy()
                    item_count_map[item_index] = count

                    try:
                        message = messages[-1]
                        if message[0] != volume:
                            messages.append([volume, item_price, []])
                    except IndexError:
                        messages.append([volume, item_price, []])

                    messages[-1][2].append('    ' + str(count) + ': f' + str(item_index) + '(' + str(volume) + ') = ' + str(item_price) + ' + f' + str(item_index - 1) + '(' + str(volume - count * self.__volume_map[item_index]) + ') = ' + str(general_price))

                    if max_price <= general_price:
                        item_count = count
                        max_price = general_price
                        continue

                interval_map[volume][0] = max_price
                item_count_map = last_interval_map[volume - item_count * self.__volume_map[item_index]][1].copy()
                item_count_map[item_index] = item_count
                interval_map[volume][1] = item_count_map

                if volume == 0 or messages[-2][1] != max_price:
                    messages[-1][2].append('max: f' + str(item_index) + '(' + str(volume) + ') = ' + str(max_price))
                    messages[-1][1] = max_price
                elif volume != messages[-2][0]:
                    messages.pop()

        self.__print(messages)
        return interval_map


algorithm = BackpackTaskSolveAlgorithm(84, [25, 21, 17, 12], [99, 82, 56, 21])
print(algorithm.solve())
