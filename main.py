from keltner_indicator import keltner_channel
from bb_band_indicator import bollinger_bands
from ttm_squeeze_indicator import ttm_squeeze
from chande_indicator import calculate_cmo
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data.csv')

keltner_data = keltner_channel(data)



bb_band_data = bollinger_bands(data)

ttm_data = ttm_squeeze(data)

chande_data = calculate_cmo(data)



# plt.plot(keltner_data['high'])
# plt.plot(keltner_data['mid'])
# plt.plot(keltner_data['low'])
# plt.plot(bb_band_data['upper'])
# plt.plot(bb_band_data['low'])
# plt.plot(bb_band_data['mid'])
# plt.plot(data['Close'])
# plt.show()

all_data = pd.DataFrame({
    'price_data': data['Close'],
    #'keltner_data': keltner_data,
    'keltner_up': keltner_data['high'],
    'keltner_low': keltner_data['low'],
    'keltner_mid': keltner_data['mid'],
    #'bb_data': bb_band_data,
    'bb_upper': bb_band_data['upper'],
    'bb_lower': bb_band_data['lower'],
    'bb_mid': bb_band_data['mid'],
    # 'ttm_squeeze': ttm_data['ttm_squeeze'],
    'ttm_squeeze': (bb_band_data['lower'] > keltner_data['low']).astype(int) - (
                bb_band_data['upper'] < keltner_data['high']).astype(int)

})

#print(all_data['ttm_squeeze'])

all_data['bbu_inside_keltneru'] = all_data['keltner_up'] > all_data['bb_upper']
all_data['bbl_inside_keltnerl'] = all_data['keltner_low'] < all_data['bb_lower']
all_data['bb_inside_keltner'] = (all_data['keltner_up'] > all_data['bb_upper']) & (all_data['keltner_low'] < all_data['bb_lower'])


chande_data = pd.DataFrame({
    'chande': chande_data
})

all_data['chande_threshold'] = (chande_data['chande'] > -1) & (chande_data['chande'] < 1)

print(all_data['chande_threshold'].any())

#print(all_data['chande_threshold'])

#print(all_data['chande_threshold'])




all_data = all_data.dropna()

# for element in all_data['bbl_inside_keltnerl']:
#     if element:
#         print('True')

# for element in all_data['bbu_inside_keltneru']:
#     if element:
#         print('True')

# for element in all_data['bb_inside_keltner']:
#     if element:
#         print('True')

#print(all_data['bbl_inside_keltnerl'].any())


# plt.plot(all_data['bb_lower'])
# plt.plot(all_data['keltner_low'])
# plt.show()




# Create a grid of subplots with 2 rows and 1 column
# The top subplot (for the price data) is 3 times the height of the bottom subplot (for the TTM Squeeze)
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=3)
ax2 = plt.subplot2grid((6,1), (3,0), rowspan=1)
ax3 = plt.subplot2grid((6,1), (4,0), rowspan=2)


# Plot 'price_data' on the y-axis and the DataFrame index on the x-axis in the top subplot
ax1.plot(all_data.index, all_data['price_data'], label='Price Data')
ax3.plot(chande_data.index, chande_data, label='chande')
# Create a boolean mask for the points where both 'bbu_inside_keltneru' and 'bbl_inside_keltnerl' are True
mask_bb_kc = (all_data['bbu_inside_keltneru'] == True) & (all_data['bbl_inside_keltnerl'] == True)


# Create the mask for the new condition
mask_chande = all_data['chande_threshold'] == True


# Plot purple dots for the points where chande_threshold is True
ax1.plot(all_data.index[mask_chande], all_data['price_data'][mask_chande], 'mo', label='Chande Threshold')

# Plot green dots for the points where both conditions are True in the top subplot
ax1.plot(all_data.index[mask_bb_kc], all_data['price_data'][mask_bb_kc], 'go', label='Bollinger Bands Inside Keltner Channel')
ax1.plot()
# Plot TTM Squeeze in the bottom subplot as a histogram
# Plot bars above x-axis for squeeze period and below x-axis for normal period
ax2.bar(all_data.index, all_data['ttm_squeeze'], label='TTM Squeeze', color='blue')

# Set y-limits to clearly visualize both squeeze and normal periods
ax2.set_ylim(-1.5, 1.5)

ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title('Price Data and TTM Squeeze Indicator')
ax1.legend()

ax2.set_xlabel('Date')
ax2.set_ylabel('TTM Squeeze')
ax2.legend()

plt.tight_layout()
plt.show()
