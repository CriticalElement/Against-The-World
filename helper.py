import pygame


__all__ = ('gravity', 'cof', 'rotate_image_along_topleft_pivot', 'rotate_image_along_bottomleft_pivot',
           'rotate_along_pivot')


gravity = -1  # default constant for gravity
cof = 0.9  # default constant for the coefficient of friction


def rotate_image_along_topleft_pivot(sprite, original_surface, degree):
    rotated = pygame.transform.rotate(original_surface, degree)
    new_rect = rotated.get_rect(topleft=sprite.rect.topleft)
    size_off_x = 0 - (new_rect.width - sprite.rect.width) / 2
    size_off_y = 0 - (new_rect.height - sprite.rect.height) / 2
    new_rect = rotated.get_rect(topleft=(sprite.rect.x + size_off_x,
                                         sprite.rect.y + size_off_y))
    return new_rect, rotated


def rotate_image_along_bottomleft_pivot(sprite, original_surface, degree):
    rotated = pygame.transform.rotate(original_surface, degree)
    new_rect = rotated.get_rect(topleft=sprite.rect.topleft)
    size_off_x = 0 - (new_rect.width - sprite.rect.width) / 2
    size_off_y = 0 - (new_rect.height - sprite.rect.height) / 2
    new_rect = rotated.get_rect(topleft=(sprite.rect.x + size_off_x,
                                         sprite.rect.y + size_off_y))
    return new_rect, rotated


def rotate_along_pivot(sprite, pos, pivot, angle):
    # offset from pivot to center
    image_rect = sprite.original_surface.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(sprite.original_surface, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image_rect, rotated_image
